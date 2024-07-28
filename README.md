# Cat-Image-Marketplace-Snippet


Check out these code snippets and application GIFs demonstrating the Cat Image Marketplace in action!


## Files

1. **routes.py**: This files uses Flask application to manage user authentication and cat image marketplace. It provides routes for logging in, signing up, and logging out, with user emails encrypted for security. Users can view, buy, and sell cat images, with transactions and ownership tracked via a blockchain like system. The application includes functionality for editing cat images, viewing transaction history, and ensuring secure token transactions. It protects sensitive routes using session management and a login_required decorator.

2. **database.py**: The code defines a database class for managing MySQL operations, including database connection, table creation, and data insertion. It handles database queries, creates tables from SQL files, and inserts rows with specified columns and parameters. Additionally, it initializes encryption settings for password security and reversible encryption for data protection.

3. **marketplacesell.html**: This file extends a html layout and uses Jinja to display the user's token balance and list their owned cat imagess. It includes a form for uploading or creating cat images, with fields for description, token value, and file upload. Jinja conditions and loops handle displaying existing NFTs with options to edit their details, or show a message if no imagess are owned.

4. **marketplacebuy.html**: The HTML template presents a page for purchasing cat images. It displays the user's token balance and iterates through available cat images, showing their images, descriptions, and token prices. Users can buy images via a form that posts the image's ID. If no images are available, a message is shown. The template extends a shared layout and relies on Jinja for injecting dynamic content.
   


## App Demo
