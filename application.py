from flask import Flask, request, jsonify , render_template
from model import recommend_products,top5_products,check_valid_user

app = Flask(__name__)
output=''
@app.route('/')
def home():
    return render_template('login.html', username=None, recommendations=None, error_message=None)

@app.route('/predict', methods=['POST'])
def recommend():
    print('in')
    if request.method=='POST':
        username=request.form.get('username')

    if not username:
        error = "Username is required"
        return render_template('login.html', recommendations=None, error_message=error)
    else:
        flag=check_valid_user(username)
        if flag==False:
            error = "Invalid Username"
            return render_template('login.html', recommendations=None, error_message=error)


    top20_products = recommend_products(username)
    get_top5_recommendations = top5_products(top20_products)
    print(get_top5_recommendations)
    return render_template('login.html',username=username, recommendations=get_top5_recommendations.name.tolist(), error_message=None)

if __name__ == '__main__':
    app.run(debug=True)