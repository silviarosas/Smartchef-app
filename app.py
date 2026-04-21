import streamlit as st
from openai import OpenAI
import os

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

st.set_page_config(
    page_title="SmartChef AI",
    page_icon="👩‍🍳",
    layout="centered"
)

st.title("👩‍🍳 SmartChef")
st.caption("Smart cooking based on your ingredients, budget, and AI")
st.divider()

# Initialize
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# Use it
st.subheader("❤️ Favorites")

if st.session_state["favorites"]:
    for fav in st.session_state["favorites"]:
        st.write(f"{fav['name']} 💰 ${fav['price']}")
else:
    st.info("No favorites yet")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_recipe(recipe, user_ingredients):
    prompt = f"""
    User has: {user_ingredients}
    Recipe: {recipe['name']}
    Ingredients: {recipe['ingredients']}
    Missing: {recipe['missing']}

    Explain briefly if they can cook it and why it's good.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# UI
st.set_page_config(page_title="SmartChef AI", page_icon="👩‍🍳")

st.title("👩‍🍳 SmartChef AI")
st.caption("Cook smart. Save money. Eat better.")

ingredients_input = st.text_input("Ingredients (comma separated)")
budget = st.number_input("Budget", min_value=0, value=50)

# Recipes
recipes = {
    "rice": {
        "name": "🍚 Rice",
        "ingredients": ["rice", "water", "salt"],
        "price": 30,
        "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c",
        "steps": ["Boil water", "Add rice", "Cook 15 min"]
    },
    "egg": {
        "name": "🍳 Omelette",
        "ingredients": ["egg"],
        "price": 20,
        "image": "https://images.unsplash.com/photo-1510693206972-df098062cb71",
        "steps": ["Beat eggs", "Cook in pan"]
    }
}

# Button
if st.button("Find Recipes"):

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
            "price": recipe["price"],
            "image": recipe["image"],
            "ingredients": recipe["ingredients"]
        })

    results.sort(key=lambda x: (-x["score"], x["price"]))

    if results:
     for i, r in enumerate(results[:3]):

        with st.container():
            st.markdown(f"## {r['name']} 💰 ${r['price']}")

            st.image(r["image"], use_container_width=True)

            # Labels
            if i == 0:
                st.success("⭐ Best option")

            if r["missing"]:
                st.warning(f"Missing: {', '.join(r['missing'])}")
            else:
                st.success("✅ You have everything")

            # Save button (no duplicates)
            if r["name"] not in [f["name"] for f in st.session_state.favorites]:
                if st.button(f"❤️ Save {r['name']}", key=r["name"]):
                    st.session_state.favorites.append(r)
                    st.success("Saved!")
            else:
                st.info("❤️ Already saved")

            # AI explanation
            with st.expander("🤖 SmartChef AI"):
                ai_text = explain_recipe(r, ingredients_user)
                st.write(ai_text)

            # Steps
            with st.expander("👨‍🍳 Steps"):
                for step in r["steps"]:
                    st.write("•", step)

            st.divider()
