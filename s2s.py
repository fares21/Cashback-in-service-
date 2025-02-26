from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# استقبال بيانات الطلبات من AliExpress
@app.route('/aliexpress-s2s', methods=['POST'])
def receive_s2s():
    data = request.json
    user_id = data.get('user_id')  # معرف المستخدم من الرابط
    commission = data.get('commission_earned')  # العمولة المكتسبة

    if user_id and commission:
        update_user_balance(user_id, float(commission))
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

def update_user_balance(user_id, amount):
    conn = sqlite3.connect("cashback.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE tg_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(port=5000)