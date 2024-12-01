import pygame

class Label:
    def __init__(self, pos, text_input, font, base_colour, rotate_angle = 0):
        # Assign the image to the button
        # Set the x and y positions of the button
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        # Set the text input for the button
        self.text_input = text_input
        # Set the font for the button text
        self.font = font
        # colour of the label
        self.base_colour = base_colour
        # Set the rotate angle
        self.rotate_angle = rotate_angle
        # Render the text with the base colour
        self.image = pygame.transform.rotate(self.font.render(self.text_input, True, self.base_colour), self.rotate_angle)
        # Get the rectangle area of the button image for positioning
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
		

    # Method to update the button on the screen
    def update(self, screen):
        # draw it on the screen
        screen.blit(self.image, self.rect)

class Button(Label):
    # Constructor to initialize the button object with various attributes
    def __init__(self,name, pos, text_input, font, base_colour, hovering_colour, rotate_angle = 0, image = None):
        super().__init__(pos, text_input, font, base_colour, rotate_angle)
        self.name = name
        if image:
            self.image = pygame.transform.rotate(self.font.render(self.text_input, True, self.base_colour), self.rotate_angle)
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.hovering_colour = hovering_colour     

    # Method to check if the button is clicked based on the mouse position
    def IfButtonClicked(self, position):
        # Check if the mouse position is within the button's rectangle area
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # Method to change the button text colour when hovering
    def changeColour(self, position):
        # If the mouse position is within the button's rectangle area, change text colour to hovering colour
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = pygame.transform.rotate(self.font.render(self.text_input, True, self.hovering_colour), self.rotate_angle)
        # Otherwise, change text colour back to base colour
        else:
            self.image = pygame.transform.rotate(self.font.render(self.text_input, True, self.base_colour), self.rotate_angle)
    






