## Technologies Used

This project uses the following technologies:
<img src="./Python-programming-logo-on-transparent-background-PNG.png" width="100"/>
<img src="./Android-icon-on-transparent--background-PNG.png" width="100"/>
<img src="./MySQL-Logo.wine.png" width="100"/>
<img src="./Flask_(web_framework)-Logo.wine.png" width="100"/>

# DigiApp - A Kivy-based Mobile Application

## Overview

DigiApp is a mobile application built using the Kivy framework, designed to provide a seamless and interactive user experience. It fetches data from external APIs, processes it, and displays products, images, and other related information. The app also checks for updates, handles multiple screens, and supports various user interactions with dynamic content.

### Key Features:
- Fetches and displays data from external APIs
- Multi-screen support with dynamic content
- Interactive carousel for product images
- Automatic screen switching with animations
- Version checking and update prompt
- Support for RTL languages (Arabic)

### Project Video:

[![Radin Sport - Android App](https://img.youtube.com/vi/PQA1sskEF60/0.jpg)](https://youtube.com/shorts/PQA1sskEF60?feature=share)

## Installation

### Requirements:
- Python 3.7 or higher
- Kivy 2.0+
- KivyMD for Material Design components
- `requests` for API requests
- `arabic_reshaper` and `bidi` for RTL text rendering

You can install the required dependencies using pip:

```bash
pip install kivy kivymd requests arabic-reshaper bidi
```

### Running the Application:
To run the application, simply execute the following command:

```bash
python main.py
```

This will start the app and load the main screen where dynamic content is displayed.

## Features

### Multi-Screen Navigation
The app uses multiple screens to display various sections like:

- **SplashScreen**: Initial screen displayed while data is being fetched.
- **MainScreen**: The primary screen displaying product information and images.
- **Error Connection Screen**: Displayed when there is an issue with network connectivity.
- **Product Screen**: Displays detailed information about products.
- **Account Screen**: User account details.
- **Search Screen**: Allows users to search for products.

### API Integration
The app fetches data from two external APIs:
- `https://mahdiemadi.ir/api_1`: Fetches product data, including titles, descriptions, prices, and images.
- `https://mahdiemadi.ir/api_2`: Fetches additional product details for grouping and categorization.

The app processes the fetched JSON data and displays it dynamically in the main screen's scrollable list.

### Update Check
The app checks for updates at startup by comparing the current version with the latest available version. If a new version is found, a prompt will be displayed asking the user if they wish to update.

### RTL Language Support
The application supports Right-to-Left (RTL) languages like Arabic, using the arabic_reshaper and bidi libraries. This ensures that Arabic text is displayed properly in the app.

### Dynamic Content Loading
- **Carousel**: A rotating carousel for product images that updates automatically every 3 seconds.
- **Scroll Views**: Products are displayed in scrollable lists, with detailed information such as price, discount, and product images.

## Structure

```plaintext
.
├── main.py                 # Main application file
├── main.kv                 # Kivy UI file
├── img/                    # Images used in the app
│   ├── loading1.zip        # Loading animation
│   ├── Loader_error_image.png # Error image
├── font/                   # Font files for text rendering
│   ├── IRANSansXFaNum-Medium.ttf # Persian font file
└── PYs/                    # Python class files
    ├── my_classes.py       # Custom classes used in the app
```

### Main Screens
- **SplashScreen**: Displays during the initial load while the app fetches data from the APIs.
- **MainScreen**: Displays a carousel of product images and details fetched from the APIs. Allows smooth navigation to other screens like Product, Search, and Account.
- **Error Connection Screen**: Shown if there’s an issue connecting to the network or fetching data from the API.
- **Product Screen**: Displays detailed information about a product, including title, description, price, and images.
- **Account Screen**: Displays user account details (currently minimal).
- **Search Screen**: Allows users to search for products by name or category.

### Helper Functions
- **heavy_processing**: Runs in a separate thread and fetches data from the APIs.
- **create_first_page**: Populates the main screen with product data once it has been fetched.
- **check_for_update**: Checks if the app version is up-to-date and prompts the user to update if needed.

### Error Handling
The app gracefully handles errors during API requests using try-except blocks. If there is a connection error or data decoding issue, the app will display an error screen with appropriate messaging.

### Multithreading
API calls are made in a separate thread to ensure that the UI remains responsive during data fetching. This is done using Python’s threading module, and the mainthread decorator is used to update the UI from the background thread.

## Contributing
If you’d like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request. All contributions are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- **Kivy**: For the framework used to build the application.
- **KivyMD**: For the Material Design components.
- **Requests**: For making API requests.
- **Arabic Reshaper & Bidi**: For handling RTL text rendering.

## Author
[Mehdi Emadi] – Developer  
Email: [mahdi.emadi@yahoo.com]
