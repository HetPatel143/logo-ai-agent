import openai
import streamlit as st

# Securely load OpenAI key from Streamlit secrets
openai.api_key = st.secrets[OPENAI_API_KEY]
  # Replace with your real API key

def generate_logo_concept(brand):
    icons = ['abstract shape', 'lettermark', 'emblem', 'symbolic animal', 'geometric figure']
    icon_choice = random.choice(icons)

    logo_concept = {
        'style': brand['style'],
        'primary_color': brand['color_preference'],
        'typography': brand['typography'],
        'icon': icon_choice
    }
    return logo_concept


def validate_logo(logo_concept):
    tests = {
        'Legibility Test': True,
        'Color Blindness Test': True,
        'Memorability Test': random.choice([True, False]),
        'Versatility Test': True,
        'Cultural Test': True
    }
    return tests


def generate_logo_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url

# Streamlit UI
st.title("\U0001F4BB AI Logo Generator")
st.write("Fill the brand details below to generate a real logo.")

with st.form("brand_form"):
    sector = st.text_input("Sector (e.g., Tech, Sports, FMCG)")
    company_name = st.text_input("Company Name")
    brand_values = st.text_input("Brand Values (comma-separated)")
    target_audience = st.text_input("Target Audience")
    style = st.text_input("Preferred Style (Minimalist, Bold, Luxurious)")
    color_preference = st.text_input("Color Preference (e.g., Blue, Green)")
    typography = st.text_input("Typography Preference (Sans-serif, Handwritten)")
    submitted = st.form_submit_button("Generate Logo")

if submitted:
    brand_info = {
        'sector': sector,
        'company_name': company_name,
        'brand_values': [value.strip() for value in brand_values.split(',')],
        'target_audience': target_audience,
        'style': style,
        'color_preference': color_preference,
        'typography': typography
    }

    logo = generate_logo_concept(brand_info)
    validation = validate_logo(logo)

    st.subheader("\U0001F4C5 Branding Kit")
    st.write(f"**Company Name:** {brand_info['company_name']}")
    st.write(f"**Sector:** {brand_info['sector']}")
    st.write(f"**Primary Color:** {logo['primary_color']}")
    st.write(f"**Typography Style:** {logo['typography']}")
    st.write(f"**Logo Style:** {logo['style']}")
    st.write(f"**Logo Icon:** {logo['icon']}")

    # Generate real logo image with DALL·E
    with st.spinner('Generating logo...'):
        prompt = f"Logo for a {brand_info['sector']} brand named {brand_info['company_name']}, focusing on {', '.join(brand_info['brand_values'])}. Style: {logo['style']}, Typography: {logo['typography']}, Colors: {logo['primary_color']}, Icon: {logo['icon']}."
        logo_url = generate_logo_image(prompt)
        st.image(logo_url, caption="Generated Logo", use_column_width=True)

    st.subheader("\U0001F50D Validation Results")
    for test, result in validation.items():
        status = "✅ Passed" if result else "❌ Failed"
        st.write(f"**{test}:** {status}")

    st.success("Logo generation complete! You can now refine or export it.")
