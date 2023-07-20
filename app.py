from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__, static_url_path='/static', static_folder='static/')

df1 = pd.read_csv("processed.csv")

def recommender(query, num=4):
    reco = None
    reco = pd.DataFrame(df1.nlargest(num+1, query)['Meal_name'])
    reco = reco[reco['Meal_name']!=query]

    response = ", ".join(reco["Meal_name"])

    return response


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/recommend", methods=['POST', 'GET'])
def recommend():
    if request.method=='POST':
        query = str(request.form.get('text'))

        try:
            out = recommender(query)
        except KeyError:
            out = "BBQ Chicken Wings with French Fries, Moi Moi (Steamed Bean Pudding), Donut, Chocolate Cake"


        return(render_template('index.html', response=out))

if __name__ == '__main__':
    app.run(debug=True)
