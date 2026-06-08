import logging
import uuid
import random
import asyncio
from peewee import *
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, InlineQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

TELEGRAM_TOKEN = "7073305470:AAGEUznCLlWoCpxN-e9Gp3tIuKQ1HNaGj_M" # توكنكك

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

db = SqliteDatabase('xo_unified_experience.db')

RIGHTS_TEXT = """
╭───𓆩🛡️𓆪───╮
     👨‍💻 𝘿𝙚𝙫: @avetaar  
    📢 𝘾𝙝: @EgyCodes
╰───𓆩🛡️𓆪───╯
"""

class Player(Model):
    user_id = IntegerField(unique=True)
    name = CharField()
    wins = IntegerField(default=0)
    losses = IntegerField(default=0)
    draws = IntegerField(default=0)

    class Meta:
        database = db

def new_board():
    return [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

def get_game_keyboard(board):
    keyboard = []
    for i, row in enumerate(board):
        keyboard_row = [InlineKeyboardButton(cell, callback_data=f"play_{i}_{j}") for j, cell in enumerate(row)]
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)

def check_winner(board):
    lines = (
        board[0], board[1], board[2],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    )
    for line in lines:
        if line[0] == line[1] == line[2] != " ":
            return line[0]
    if all(cell != " " for row in board for cell in row):
        return "Tie"
    return None

async def get_or_create_player(user_id, name):
    player, created = Player.get_or_create(user_id=user_id, defaults={'name': name})
    if not created and player.name != name:
        player.name = name
        player.save()
    return player

def find_game_id_by_message(message_id, context):
    for gid, gdata in context.chat_data.items():
        if isinstance(gdata, dict) and gdata.get('message_id') == message_id:
            return gid
    return None

async def start_or_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await get_or_create_player(user.id, user.first_name)
    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 العب مع البوت", callback_data="bot_difficulty")],
        [InlineKeyboardButton("👥 تحدي لاعب آخر", callback_data="init_pvp_game")],
        [InlineKeyboardButton("📊 إحصائياتي", callback_data="my_score")],
        [InlineKeyboardButton("🏆 لوحة الصدارة", callback_data="leaderboard")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = f"⚔️ أهلاً بك في ساحة X-O النهائية! ⚔️\n\nاختر وضع اللعب الذي تفضله.{RIGHTS_TEXT}"
    
    query = update.callback_query
    if query:
        await query.answer()
        try:
            await query.edit_message_text(message_text, reply_markup=reply_markup)
        except BadRequest: pass
    else:
        await update.message.reply_text(message_text, reply_markup=reply_markup)

async def bot_difficulty_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("سهل", callback_data="start_bot_easy")],
        [InlineKeyboardButton("متوسط", callback_data="start_bot_medium")],
        [InlineKeyboardButton("صعب", callback_data="start_bot_hard")],
        [InlineKeyboardButton("🏠 رجوع", callback_data="main_menu")]
    ]
    await query.edit_message_text(f"اختر مستوى صعوبة البوت:{RIGHTS_TEXT}", reply_markup=InlineKeyboardMarkup(keyboard))

async def start_bot_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    difficulty = query.data.split('_')[-1]
    game_id = f"bot_{uuid.uuid4().hex[:8]}"
    
    game_data = {
        'id': game_id, 'mode': 'bot', 'difficulty': difficulty,
        'players': {'X': {'id': query.from_user.id, 'name': query.from_user.first_name}, 'O': {'id': context.bot.id, 'name': 'الأسطورة'}},
        'board': new_board(), 'turn': 'X', 'message_id': query.message.message_id
    }
    context.chat_data[game_id] = game_data
    
    keyboard = get_game_keyboard(game_data['board'])
    await query.edit_message_text(f"لقد بدأت لعبة ضد البوت (مستوى: {difficulty}).\n\nدورك للعب (X).", reply_markup=keyboard)

def get_bot_move(board, difficulty):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    def find_winning_move(player):
        for r, c in empty_cells:
            board[r][c] = player
            if check_winner(board) == player:
                board[r][c] = " "; return r, c
            board[r][c] = " "
        return None

    if difficulty == 'hard':
        if (move := find_winning_move('O')): return move
        if (move := find_winning_move('X')): return move
    if difficulty in ['hard', 'medium'] and (1, 1) in empty_cells: return 1, 1
    
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]; random.shuffle(corners)
    for r, c in corners:
        if (r, c) in empty_cells: return r, c
    return random.choice(empty_cells)

async def init_pvp_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.message.chat.type == 'private':
        game_id = f"pvp_{uuid.uuid4().hex[:8]}"
        context.bot_data[game_id] = {'player1_id': query.from_user.id, 'player1_name': query.from_user.first_name}
        keyboard = [[InlineKeyboardButton("🔗 إنشاء ومشاركة دعوة", switch_inline_query=game_id)]]
        await query.edit_message_text(f"✅ ممتاز! الآن اضغط على الزر أدناه واختر الصديق الذي تريد دعوته للعب.{RIGHTS_TEXT}", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        player1 = query.from_user
        game_id = f"pvp_{uuid.uuid4().hex[:8]}"
        game_data = {
            'id': game_id, 'mode': 'pvp_group',
            'players': {'X': {'id': player1.id, 'name': player1.first_name}, 'O': None},
            'board': None, 'turn': 'X', 'message_id': query.message.message_id
        }
        context.chat_data[game_id] = game_data
        keyboard = [[InlineKeyboardButton("⚔️ قبول التحدي", callback_data=f"join_{game_id}")]]
        await query.edit_message_text(f"📣 اللاعب {player1.first_name} بدأ تحدياً!\n\nننتظر لاعباً آخر...", reply_markup=InlineKeyboardMarkup(keyboard))
        context.job_queue.run_once(expire_challenge, 60, data={'chat_id': query.message.chat_id, 'message_id': query.message.message_id, 'game_id': game_id}, name=f"expire_{game_id}")

async def expire_challenge(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    game_id = job_data['game_id']
    if game_id in context.chat_data and context.chat_data[game_id]['players']['O'] is None:
        try:
            await context.bot.edit_message_text(f"⌛️ انتهت صلاحية هذا التحدي.{RIGHTS_TEXT}", chat_id=job_data['chat_id'], message_id=job_data['message_id'])
        except BadRequest: pass
        if game_id in context.chat_data: del context.chat_data[game_id]

async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    game_id = query.data.split('_')[1]
    
    if game_id not in context.chat_data:
        await query.answer("❌ الدعوة انتهت!", show_alert=True)
        return

    game_data = context.chat_data[game_id]
    player2 = query.from_user
    if player2.id == game_data['players']['X']['id']:
        await query.answer("لا يمكنك قبول تحدي نفسك!", show_alert=True)
        return

    await query.answer("✅ لقد قبلت التحدي!")
    await get_or_create_player(player2.id, player2.first_name)
    
    game_data['players']['O'] = {'id': player2.id, 'name': player2.first_name}
    game_data['board'] = new_board()
    
    p1_name = game_data['players']['X']['name']
    p2_name = game_data['players']['O']['name']
    
    keyboard = get_game_keyboard(game_data['board'])
    await query.edit_message_text(f"🎉 {p1_name} (X) ضد {p2_name} (O).\n\nالدور الآن للاعب (X) - {p1_name}.", reply_markup=keyboard)
    
    if (jobs := context.job_queue.get_jobs_by_name(f"expire_{game_id}")):
        for job in jobs: job.schedule_removal()

async def play_move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    game_id = find_game_id_by_message(query.message.message_id, context)
    if not game_id:
        await query.answer("هذه اللعبة انتهت.", show_alert=True)
        return
    
    game_data = context.chat_data[game_id]
    user_id = query.from_user.id
    turn = game_data['turn']
    
    if user_id != game_data['players'][turn]['id']:
        await query.answer("ليس دورك!", show_alert=True)
        return

    await query.answer()
    _, r, c = query.data.split('_')
    r, c = int(r), int(c)
    board = game_data['board']

    if board[r][c] != " ":
        await query.answer("هذا المربع مشغول!", show_alert=True)
        return

    board[r][c] = turn
    winner = check_winner(board)

    if winner:
        await handle_game_end(update, context, winner, game_id)
        return

    game_data['turn'] = "O" if turn == "X" else "X"
    
    if game_data['mode'] == 'bot' and game_data['turn'] == 'O':
        await update_board_and_trigger_bot(update, context, game_id)
    else:
        await update_board(update, context, game_id)

async def update_board_and_trigger_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, game_id: str):
    query = update.callback_query
    game_data = context.chat_data[game_id]
    
    await query.edit_message_text(f"دورك (X). يفكر {game_data['players']['O']['name']} (O)...", reply_markup=get_game_keyboard(game_data['board']))
    await asyncio.sleep(1)
    
    bot_move = get_bot_move(game_data['board'], game_data['difficulty'])
    r, c = bot_move
    game_data['board'][r][c] = 'O'
    
    if (winner := check_winner(game_data['board'])):
        await handle_game_end(update, context, winner, game_id)
        return
        
    game_data['turn'] = 'X'
    await update_board(update, context, game_id)

async def update_board(update: Update, context: ContextTypes.DEFAULT_TYPE, game_id: str):
    query = update.callback_query
    game_data = context.chat_data[game_id]
    next_player_name = game_data['players'][game_data['turn']]['name']
    message = f"الدور الآن للاعب ({game_data['turn']}) - {next_player_name}."
    
    try:
        await query.edit_message_text(text=message, reply_markup=get_game_keyboard(game_data['board']))
    except BadRequest: pass

async def handle_game_end(update, context, winner, game_id):
    query = update.callback_query
    game_data = context.chat_data[game_id]
    
    p1 = await get_or_create_player(game_data['players']['X']['id'], game_data['players']['X']['name'])
    p2_data = game_data['players']['O']
    p2 = await get_or_create_player(p2_data['id'], p2_data['name']) if p2_data['id'] != context.bot.id else None

    end_message = ""
    if winner == "Tie":
        if p2: p1.draws += 1; p2.draws += 1
        end_message = "🤝 تعادل!"
    else:
        winner_player_data = game_data['players'][winner]
        winner_player = p1 if winner == 'X' else p2
        loser_player = p2 if winner == 'X' else p1
        if winner_player: winner_player.wins += 1
        if loser_player: loser_player.losses += 1
        end_message = f"🎉 الفائز هو {winner_player_data['name']} ({winner})!"
    
    p1.save()
    if p2: p2.save()
    
    final_message = f"{end_message}\n\nاضغط على الزر للعودة للقائمة الرئيسية."
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]])
    await query.edit_message_text(text=final_message, reply_markup=keyboard)
    del context.chat_data[game_id]

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if "اكس او" in query.lower() or "xo" in query.lower():
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="🎲 تحدي X-O",
                description="اضغط هنا لإرسال تحدي لعبة X-O في هذه المحادثة.",
                input_message_content=InputTextMessageContent("."),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 ابدأ تحدي X-O", callback_data="init_pvp_game")]])
            )
        ]
        await update.inline_query.answer(results, cache_time=1)
    elif query.startswith("pvp_"):
        game_id = query
        if game_id in context.bot_data:
            p1_name = context.bot_data[game_id]['player1_name']
            results = [
                InlineQueryResultArticle(
                    id=game_id,
                    title="🎲 دعوة للعبة X-O",
                    description=f"اضغط لإرسال الدعوة من {p1_name}.",
                    input_message_content=InputTextMessageContent(f"أنا أدعوك للعبة X-O ضدي!"),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ قبول الدعوة", callback_data=f"accept_{game_id}")]])
                )
            ]
            await update.inline_query.answer(results, cache_time=0)

async def accept_private_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    game_id_pvp = query.data.split('_')[1]
    player2 = query.from_user

    if game_id_pvp not in context.bot_data:
        await query.edit_message_text(f"❌ هذه الدعوة قديمة أو منتهية.{RIGHTS_TEXT}")
        return

    game_info = context.bot_data[game_id_pvp]
    player1_id = game_info['player1_id']
    if player2.id == player1_id:
        await query.answer("لا يمكنك قبول دعوتك الخاصة!", show_alert=True)
        return

    new_game_id = f"private_{uuid.uuid4().hex[:8]}"
    context.chat_data[new_game_id] = {
        'id': new_game_id, 'mode': 'pvp_private',
        'players': {'X': {'id': player1_id, 'name': game_info['player1_name']}, 'O': {'id': player2.id, 'name': player2.first_name}},
        'board': new_board(), 'turn': 'X', 'message_id': query.message.message_id
    }
    
    del context.bot_data[game_id_pvp]
    
    p1_name = context.chat_data[new_game_id]['players']['X']['name']
    p2_name = context.chat_data[new_game_id]['players']['O']['name']
    
    keyboard = get_game_keyboard(context.chat_data[new_game_id]['board'])
    await query.edit_message_text(f"🎉 {p1_name} (X) ضد {p2_name} (O).\n\nالدور الآن للاعب (X) - {p1_name}.", reply_markup=keyboard)

async def my_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    player = await get_or_create_player(user.id, user.first_name)
    score_text = f"📊 سجلك يا {player.name}:\n🏆 فوز: {player.wins}\n❌ خسارة: {player.losses}\n🤝 تعادل: {player.draws}{RIGHTS_TEXT}"
    await query.edit_message_text(score_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 رجوع", callback_data="main_menu")]]))

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    top_players = Player.select().order_by(Player.wins.desc()).limit(5)
    leaderboard_text = "🏆 أفضل 5 لاعبين:\n\n" + ("\n".join([f"{i+1}. {p.name} - {p.wins} فوز" for i, p in enumerate(top_players)]) or "لا يوجد لاعبون بعد.")
    await query.edit_message_text(f"{leaderboard_text}{RIGHTS_TEXT}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 رجوع", callback_data="main_menu")]]))

def main() -> None:
    db.connect()
    db.create_tables([Player])
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_or_trigger, filters.ChatType.PRIVATE))
    application.add_handler(MessageHandler(filters.Regex(r'^(اكس او|xo)$') & filters.ChatType.GROUPS, start_or_trigger))
    
    application.add_handler(CallbackQueryHandler(show_main_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(bot_difficulty_menu, pattern="^bot_difficulty$"))
    application.add_handler(CallbackQueryHandler(start_bot_game, pattern=r'^start_bot_'))
    application.add_handler(CallbackQueryHandler(init_pvp_game, pattern="^init_pvp_game$"))
    application.add_handler(CallbackQueryHandler(join_game, pattern=r'^join_'))
    application.add_handler(CallbackQueryHandler(my_score, pattern="^my_score$"))
    application.add_handler(CallbackQueryHandler(leaderboard, pattern="^leaderboard$"))
    application.add_handler(CallbackQueryHandler(play_move, pattern=r'^play_'))
    application.add_handler(CallbackQueryHandler(accept_private_game, pattern=r'^accept_'))
    application.add_handler(InlineQueryHandler(inline_query))

    print("⚔️ بوت X-O (النسخة النهائية المخصصة) قيد التشغيل...")
    application.run_polling()

if __name__ == "__main__":
    main()
