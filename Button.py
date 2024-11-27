class Button:
    # Constructor to initialize the button object with various attributes
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        # Assign the image to the button
        self.image = image
        # Set the x and y positions of the button
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        # Set the font for the button text
        self.font = font
        # Set the base and hovering colors for the button text
        self.base_color, self.hovering_color = base_color, hovering_color
        # Set the text input for the button
        self.text_input = text_input
        # Render the text with the base color
        self.text = self.font.render(self.text_input, True, self.base_color)
        # If no image is provided, use the rendered text as the button image
        if self.image is None:
            self.image = self.text
        # Get the rectangle area of the button image for positioning
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # Get the rectangle area of the text for positioning
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
		

    # Method to update the button on the screen
    def update(self, screen):
        # If an image is provided, draw it on the screen
        if self.image is not None:
            screen.blit(self.image, self.rect)
        # Draw the text on the screen
        screen.blit(self.text, self.text_rect)

    # Method to check if the button is clicked based on the mouse position
    def IfButtonClicked(self, position):
        # Check if the mouse position is within the button's rectangle area
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # Method to change the button text color when hovering
    def changeColor(self, position):
        # If the mouse position is within the button's rectangle area, change text color to hovering color
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        # Otherwise, change text color back to base color
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    






