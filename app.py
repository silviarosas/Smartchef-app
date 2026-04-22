import streamlit as st
from openai import OpenAI

# Page config (ONLY ONCE)
st.set_page_config(page_title="SmartChef AI", page_icon="👩‍🍳", layout="centered")

# Session state
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def explain_recipe(recipe, user_ingredients):
    try:
        prompt = f"""
        User has: {user_ingredients}
        Recipe: {recipe['name']}
        Ingredients: {recipe['ingredients']}
        Missing: {recipe['missing']}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        return "⚠️ AI temporarily unavailable"

# UI
st.title("👩‍🍳 SmartChef")
st.caption("Smart cooking based on your ingredients, budget, and AI")
st.divider()
if r["missing"]:
    st.warning(f"Missing: {', '.join(r['missing'])}")
    st.info(f"🛒 Estimated extra cost: ${r['missing_cost']}")
else:
    st.success("✅ You have everything")

# Inputs
ingredients_input = st.text_input("Ingredients (comma separated)")
budget = st.number_input("Budget", min_value=0, value=50)

# Recipes
recipes = {
    "rice": {
        "name": "🍚 Rice",
        "ingredients": ["rice", "water", "salt"],
        "price": 30,
        "ingredients prices": {
            "rice": 25,
            "water": 0,
            "salt": 5,
        },
         "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c",
        "steps": ["Boil water", "Add rice", "Cook 15 min"]
    },
    "egg": {
        "name": "🍳 Omelette",
        "ingredients": ["egg"],
        "price": 20,
        "ingredients prices": {
            "egg": 10,
            "onion":5,
            "salt":5,
        },
        "image": "https://images.unsplash.com/photo-1510693206972-df098062cb71",
        "steps": ["Beat eggs", "Cook in pan"]
    }
}

st.subheader("🛒 Shopping List")

shopping_list = set()

for r in results[:3]:
    for item in r["missing"]:
        shopping_list.add(item)

if shopping_list:
    for item in shopping_list:
        st.write(f"- {item}")
else:
    st.success("You don’t need to buy anything 🎉")
    


# FIND RECIPES
if st.button("Find Recipes"):

    ingredients_user = [i.strip().lower() for i in ingredients_input.split(",")]
    results = []

    for recipe in recipes.values():
        if recipe["price"] > budget:
            continue

        match_count = sum(1 for item in recipe["ingredients"] if item in ingredients_user)
        missing = [item for item in recipe["ingredients"] if item not in ingredients_user]

        missing_cost = sum(
    recipe["ingredient_prices"].get(item, 10)
    for item in missing
)

        score = match_count / len(recipe["ingredients"])

        results.append({
    "name": recipe["name"],
    "steps": recipe["steps"],
    "missing": missing,
    "missing_cost": missing_cost,
    "score": score,
    "price": recipe["price"],
    "image": recipe["image"],
    "ingredients": recipe["ingredients"]
}),

    results.sort(key=lambda x: (-x["score"], x["price"]))

    if results:

        # 🔥 SHOW TOP 3 RECIPES (NO AI YET)
        for i, r in enumerate(results[:3]):

            with st.container():
                st.markdown(f"## {r['name']} 💰 ${r['price']}")
                st.image(r["image"], use_container_width=True)

                if i == 0:
                    st.success("⭐ Best option")

                if r["missing"]:
                    st.warning(f"Missing: {', '.join(r['missing'])}")
                else:
                    st.success("✅ You have everything")

                # Save button
                if r["name"] not in [f["name"] for f in st.session_state["favorites"]]:
                    if st.button(f"❤️ Save {r['name']}", key=r["name"]):
                        st.session_state["favorites"].append(r)
                        st.success("Saved!")
                else:
                    st.info("❤️ Already saved")

                # Steps
                with st.expander("👨‍🍳 Steps"):
                    for step in r["steps"]:
                        st.write("•", step)

                st.divider()

        # 🔥 AI ONLY FOR BEST RECIPE
        best = results[0]

        st.subheader("🤖 SmartChef AI Recommendation")

        if st.button("Get AI Advice"):
            ai_text = explain_recipe(best, ingredients_user)
            st.write(ai_text)

# FAVORITES
st.subheader("❤️ Favorites")

if st.session_state["favorites"]:
    for fav in st.session_state["favorites"]:
        st.write(f"{fav['name']} 💰 ${fav['price']}")
else:
    st.info("No favorites yet")
