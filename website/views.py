from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .dbconnect import connect_to_database
import time
import json
import ast

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/newfundme", methods=["GET", "POST"])
def newfundme():
    connection = connect_to_database()
    cursor = connection.cursor()
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        goal = request.form.get("total_funding")
        image_link = request.form.get("image_link")
        values = (title, description, goal, image_link, current_user.id)
        query = "INSERT INTO crowdfund (title, description, goal, image, username) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, values)
        connection.commit()
        connection.close()
        flash("FundMe Created!", category="success")

        return redirect(url_for("views.projects"))
    return render_template("newfundme.html", user=current_user)

@views.route("/projects", methods=["GET", "POST"])
def projects():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM crowdfund"

    cursor.execute(query)

    projects = cursor.fetchall()
    connection.close()
    return render_template("projects.html", user=current_user, projects=projects)

@views.route("myprojects", methods=["GET", "POST"])
def myprojects():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM crowdfund WHERE username = %s"
    cursor.execute(query, (current_user.id,))

    projects = cursor.fetchall()
    connection.close()
    return render_template("myprojects.html", user=current_user, projects=projects)

@views.route("/editfundme/<string:id>", methods=["GET", "POST"])
def editfundme(id):
    connection = connect_to_database()
    cursor = connection.cursor()

    if request.method == "POST":
        new_title = request.form.get("title")
        new_description = request.form.get("description")
        new_image = request.form.get("image")
        new_goal = request.form.get("total_funding")

        query = "UPDATE crowdfund SET title = %s, description = %s, image = %s, goal = %s WHERE title = %s"
        cursor.execute(query, (new_title, new_description, new_image, new_goal, id))
        connection.commit()

        connection.close()
        flash("Project updated successfully!", "success")
        return redirect(url_for("views.myprojects"))

    query = "SELECT * FROM crowdfund WHERE title = %s"
    cursor.execute(query, (id,))
    project = cursor.fetchone()
    connection.close()

    return render_template("editfundme.html", user=current_user, project=project)

@views.route("/deletefundme/<string:id>", methods=["GET", "POST"])
def deletefundme(id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "DELETE FROM crowdfund WHERE title = %s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()
    flash("Project deleted successfully!", "success")
    return redirect(url_for("views.myprojects"))

@views.route("/careers")
def careers():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM careers"
    cursor.execute(query)

    careers = cursor.fetchall()
    return render_template("careers.html", careers=careers)

@login_required
@views.route("/mycareers")
def mycareers():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM careers WHERE username = %s"
    cursor.execute(query, (current_user.id,))
    mycareers = cursor.fetchall()
    connection.close()
    return render_template("mycareers.html", user=current_user, mycareers=mycareers)

@views.route("/newcareers", methods=["GET", "POST"])
def newcareers():
    connection = connect_to_database()
    cursor = connection.cursor()
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        contact = request.form.get("contact")
        image_link = request.form.get("image_link")
        values = (title, description, contact, image_link, current_user.id)
        query = "INSERT INTO careers (title, description, contact, image, username) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, values)
        connection.commit()
        connection.close()
        flash("Career Opportunity Posted", category="success")

        return redirect(url_for("views.careers"))
    return render_template("newcareers.html", user=current_user)


@views.route("/deletecareer/<string:id>", methods=["GET", "POST"])
def deletecareer(id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "DELETE FROM careers WHERE title = %s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()
    flash("Project deleted successfully!", "success")
    return redirect(url_for("views.careers"))

@views.route("/ideavalidation", methods=["GET", "POST"])
def ideavalidation():
    connection = connect_to_database()
    cursor = connection.cursor()
    if request.method == "POST":
        product_description = request.form.get("product_description")
        target_consumer = request.form.get("target_customer_demographic")
        initial_investment = request.form.get("initial_investment")
        company_goals = request.form.get("goals_of_the_company")
        likelihood_risk = request.form.get("likelihood_of_taking_risk")
        import google.generativeai as genai

        genai.configure(api_key="AIzaSyBZhIcMakEwzjtkUgv1gV096tHlsEoxWfc")

        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        message = f"""Product: {product_description}, Target Customer Demographic: {target_consumer}, Initial Investment: {initial_investment}, Goals of the Company: {company_goals}, Tendency of taking Risk: {likelihood_risk}"""

        convo = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            """As a business analyst/mentor, you will be provided with information on Product, Target Customer Demographic, Initial Investment, Goals of the Company, and Likelihood of taking Risk. 
                            Provide a brief business report where each element is as specified:
                            A: 1 line on a general comment about overall business, include if budget is enough or too much. If insufficient budget, provide a more realistic budget. (datatype = string).
                            B: Many different possible Risks involved in this business (datatype = list).
                            C: Names of existing competitors, if any. If not, then mention that it is an innovative idea (datatype = list).
                            D: Existing Techonology that could help aid the business (datatype = list).
                            E: Effective Marketing Strategy for the business (datatype = list).
                            
                            OUTPUT FORMAT: [A,B,C,D,E]
                                                
                            If any data is NOT AVAILABLE, ignore it and provide feedback on the rest.
                            Provide very innovative suggestions if tendency of taking risk is high."""
                        ],
                    },
                    {
                        "role": "model",
                        "parts": [
                            "Okay, provide me with the company information. I will provide in the format required as to my best knowledge."
                        ],
                    },
                    {
                        "role": "user",
                        "parts": [
                            """
                            "Product: Shampoo for colored hair, Target Customer Demographic: Young Women, Initial Investment: 25,000 rupees, Goals of the Company: Make Best Shampoo for Damage Free Hair, Tendency of taking Risk: Unlikely."
                            """
                        ],
                    },
                    {
                        "role": "model",
                        "parts": [
                            """["This business venture appears to NOT have great potential as it is a saturated market and budget is also quite low", [Market competition, Product differentiation, Ingredient costs, Lack of brand awareness], [Tresemme, L'Oréal, Olaplex, Pantene, Dove, Redken], [Customer relationship management (CRM) systems, E-commerce platforms, Ingredient analysis software], [Target specific hair salons, Influencer marketing, Discounts and Promotions, Create a loyalty program]]"""
                        ],
                    },
                    {
                        "role": "user",
                        "parts": [
                            """
                            "Product: Baby food, Target Customer Demographic: Young Women, Initial Investment: 2,50,000 rupees, Goals of the Company: Make Healthiest Baby Food, Tendency of taking Risk: Likely."
                            """
                        ],
                    },
                    {
                        "role": "model",
                        "parts": [
                            """["This business venture appears to have good potential for success and the budget seems sufficient, but there are some risks to consider.", ['Market competition', 'Product differentiation', 'Changes in Consumer Preference', 'Fluctuating Product Costs'], ['Gerber', 'Earth\'s Best', 'Beech-Nut'], ['Automated inventory management systems', 'Nutritional analysis software', 'Online ordering platforms', 'Customer relationship management (CRM) systems', 'E-commerce platforms'], ['Social media marketing to reach young mothers','Partnerships with healthcare professionals','Target specific baby stores', 'Influencer marketing']]"""
                        ],
                    }
                ]
        )

        convo.send_message(message)
        data_str = convo.last.text
        data = ast.literal_eval(data_str)
        serialized_lists = [json.dumps(inner_list) for inner_list in data[1:]]
        data_for_insert = [data[0]] + serialized_lists
        insert_sql = f"INSERT INTO ideavalidation (Username, Feedback, Risks, Competitors, Technology, PR) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_sql, [current_user.id]+data_for_insert)
        connection.commit()
        connection.close()
    return render_template("ideavalidation.html", user=current_user)

@views.route("/ideafeedback", methods=["GET", "POST"])
def ideafeedback():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM ideavalidation WHERE Username = '{}' AND id = (SELECT MAX(id) FROM ideavalidation WHERE Username = '{}')".format(current_user.id, current_user.id)
    cursor.execute(query)
    row = cursor.fetchone()
    print(row)
    if row:
        # Prepare data as a dictionary
        data = {
            'id': row[0],
            'username': row[1],
            'feedback': row[2],
            'risks': ast.literal_eval(row[3]),
            'competitors': ast.literal_eval(row[4]),
            'technologies': ast.literal_eval(row[5]),
            'strategies': ast.literal_eval(row[6])
        }
        print(data)
        # Pass the data to the template
        return render_template('ideafeedback.html', data=data)
    else:
        return "No data found for username: {}".format(current_user.id)
    
@views.route("/askathena", methods=["GET", "POST"])
def askathena():
    business_idea = request.form.get("business-idea")

    if request.method == "POST":
        import google.generativeai as genai

        genai.configure(api_key="AIzaSyBZhIcMakEwzjtkUgv1gV096tHlsEoxWfc")

        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        message = f""""This is our business idea generate a feedback for us in the same format"""
        convo = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            """As a business analyst/mentor, you will be provided with information on Product, Target Customer Demographic, Initial Investment, Goals of the Company, and Likelihood of taking Risk. 
                            Provide a brief business report where each element is as specified:
                            A: 1 line on a general comment about overall business, include if budget is enough or too much. If insufficient budget, provide a more realistic budget. (datatype = string).
                            B: Many different possible Risks involved in this business (datatype = list).
                            C: Names of existing competitors, if any. If not, then mention that it is an innovative idea (datatype = list).
                            D: Existing Techonology that could help aid the business (datatype = list).
                            E: Effective Marketing Strategy for the business (datatype = list).
                            
                            OUTPUT FORMAT: [A,B,C,D,E]
                                                
                            If any data is NOT AVAILABLE, ignore it and provide feedback on the rest.
                            Provide very innovative suggestions if tendency of taking risk is high."""
                        ],
                    },
                    {
                        "role": "model",
                        "parts": [
                            "Okay, provide me with the company information. I will provide in the format required as to my best knowledge."
                        ],
                    },
                    {
                        "role": "user",
                        "parts": [
                            """
                            "Product: Shampoo for colored hair, Target Customer Demographic: Young Women, Initial Investment: 25,000 rupees, Goals of the Company: Make Best Shampoo for Damage Free Hair, Tendency of taking Risk: Unlikely."
                            """
                        ],
                    },
                    {
                        "role": "model",
                        "parts": [
                            """["This business venture appears to NOT have great potential as it is a saturated market and budget is also quite low", [Market competition, Product differentiation, Ingredient costs, Lack of brand awareness], [Tresemme, L'Oréal, Olaplex, Pantene, Dove, Redken], [Customer relationship management (CRM) systems, E-commerce platforms, Ingredient analysis software], [Target specific hair salons, Influencer marketing, Discounts and Promotions, Create a loyalty program]]"""
                        ],
                    },
                    {
                        "role": "user",
                        "parts": [
                            """
                            "Product: Baby food, Target Customer Demographic: Young Women, Initial Investment: 2,50,000 rupees, Goals of the Company: Make Healthiest Baby Food, Tendency of taking Risk: Likely."
                            """
                        ],
                    },
                    {
                        "role": "model",
                        "parts": [
                            """["This business venture appears to have good potential for success and the budget seems sufficient, but there are some risks to consider.", ['Market competition', 'Product differentiation', 'Changes in Consumer Preference', 'Fluctuating Product Costs'], ['Gerber', 'Earth\'s Best', 'Beech-Nut'], ['Automated inventory management systems', 'Nutritional analysis software', 'Online ordering platforms', 'Customer relationship management (CRM) systems', 'E-commerce platforms'], ['Social media marketing to reach young mothers','Partnerships with healthcare professionals','Target specific baby stores', 'Influencer marketing']]"""
                        ],
                    }
                ]
        )
        convo.send_message(message)
        data_str = convo.last.text
    return render_template("askathena.html", user=current_user)