import gradio as gr
import random


def pick_plate(color_choice, style_choice):
    """Generate a random license plate number based on user preferences."""
    # Generate random plate number
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numbers = ''.join(random.choices('0123456789', k=4))

    plate_number = f"{letters}-{numbers}"

    # Create styled output
    color_map = {
        "Blue": "#1E40AF",
        "Green": "#059669",
        "Red": "#DC2626",
        "Black": "#1F2937"
    }

    bg_color = color_map.get(color_choice, "#1E40AF")

    html_output = f"""
    <div style="background-color: {bg_color}; color: white; padding: 30px;
                border-radius: 10px; text-align: center; font-family: monospace;
                font-size: 48px; font-weight: bold; border: 3px solid #FFF;">
        {plate_number}
    </div>
    <p style="text-align: center; margin-top: 20px; font-size: 18px;">
        Style: {style_choice} | Color: {color_choice}
    </p>
    """

    return html_output


def create_app():
    """Create and configure the Gradio interface."""
    with gr.Blocks(title="Plate Picker") as app:
        gr.Markdown("# 🚗 Plate Picker")
        gr.Markdown("Generate random license plate numbers with custom colors and styles!")

        with gr.Row():
            with gr.Column():
                color = gr.Radio(
                    choices=["Blue", "Green", "Red", "Black"],
                    value="Blue",
                    label="Plate Color"
                )
                style = gr.Radio(
                    choices=["Standard", "Premium", "Classic", "Modern"],
                    value="Standard",
                    label="Plate Style"
                )
                generate_btn = gr.Button("Generate Plate", variant="primary")

            with gr.Column():
                output = gr.HTML(label="Your License Plate")

        generate_btn.click(
            fn=pick_plate,
            inputs=[color, style],
            outputs=output
        )

        # Generate on page load
        app.load(
            fn=pick_plate,
            inputs=[color, style],
            outputs=output
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.launch()
