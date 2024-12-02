from flask import Flask, request, jsonify, render_template
import pandas as pd

#init the flask app
app = Flask(__name__)

#load our data
drinks_df = pd.read_csv('drinks.csv')
rumors_df = pd.read_csv('rumors.csv')

#helper functions
#this gets the drink info, theoretically
def get_drink_info(drink_name):
    drink = drinks_df[drinks_df['name'].str.lower() == drink_name.lower()]
    if not drink.empty:
        info = drink.iloc[0]
        return f"{info['name']} costs {info['cost']} gold."
    else:
        return "Sorry, we don't serve that drink here!"
#this gets the rumor info, confirmed
def get_random_rumor():
    rumor = rumors_df.sample(1).iloc[0]
    return f"Rumor has it: {rumor['rumor']}. If you're curious, you can learn more at {rumor['location']}."

#routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    if 'drink' in user_message:
        drink_name = user_message.replace('drink', '').strip()
        response = get_drink_info(drink_name)
    elif 'rumor' in user_message:
        response = get_random_rumor()
    else:
        response = "I'm just a bartender. Ask me about drinks or rumors!"
    return jsonify({'response': response})

#run this biznatch
if __name__ == '__main__':
    app.run(debug=True)

