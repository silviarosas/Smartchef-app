import streamlit as st

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("👩‍🍳 SmartChef AI")

st.write("Find the best recipe based on your ingredients and budget")

# User input
ingredients_input = st.text_input("Enter your ingredients (comma separated)")
budget = st.number_input("Enter your budget", min_value=0)

if st.button("Find recipes"):
    st.write("Searching...")

import streamlit as st

st.title("👩‍🍳 SmartChef AI")

ingredients_input = st.text_input("Enter your ingredients (comma separated)")
budget = st.number_input("Enter your budget", min_value=0)

recipes = {
    "rice": {
        "name": "Simple White Rice",
        "ingredients": ["rice", "water", "salt"],
        "price": 30,
        "steps": ["Boil water", "Add rice", "Cook 15 min"]
    },
    "egg": {
        "name": "Omelette",
        "ingredients": ["egg"],
        "price": 20,
        "steps": ["Beat eggs", "Cook in pan"]
    }
}

if st.button("Find recipes"):

    ingredients_user = [i.strip().lower() for i in ingredients_input.split(",")]

    results = []

    for recipe in recipes.values():
        if recipe["price"] > budget:
            continue

        match_count = sum(1 for item in recipe["ingredients"] if item in ingredients_user)
        missing = [item for item in recipe["ingredients"] if item not in ingredients_user]

        score = match_count / len(recipe["ingredients"])

        results.append({
            "name": recipe["name"],
            "steps": recipe["steps"],
            "missing": missing,
            "score": score,
            "price": recipe["price"]
        })

    results.sort(key=lambda x: (-x["score"], x["price"]))

    if results:
        for r in results[:3]:
            st.subheader(f"{r['name']} 💰 ${r['price']}")
            
            if r["missing"]:
                st.write("Missing:", ", ".join(r["missing"]))
            else:
                st.write("✅ You have everything!")

            st.write("Steps:")
            for step in r["steps"]:
                st.write("-", step)
    else:
        st.write("No recipes found 😢")

