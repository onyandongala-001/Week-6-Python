# image_downloader.py
import os
import requests
from urllib.parse import urlparse
from datetime import datetime

def create_directory(directory_name):
    """Create directory if it doesn't exist"""
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            print(f"Directory '{directory_name}' created successfully.")
        else:
            print(f"Directory '{directory_name}' already exists.")
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False

def get_filename_from_url(url):
    """Extract filename from URL or generate one"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    
    # If URL doesn't end with a proper extension, generate a filename
    if not filename or '.' not in filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.jpg"
    
    return filename

def download_image(url, directory):
    """Download image from URL and save to directory"""
    try:
        # Send HTTP GET request
        response = requests.get(url, stream=True, timeout=30)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Check if content is an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            print(f"Warning: URL does not point to an image (Content-Type: {content_type})")
            # Continue anyway as some servers might not send proper content-type
        
        # Get filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(directory, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"File '{filename}' already exists. Skipping download.")
            return True
        
        # Download and save the image
        print(f"Downloading image from {url}...")
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Image successfully saved as '{filename}'")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function to run the image downloader"""
    print("=" * 50)
    print("IMAGE DOWNLOADER")
    print("=" * 50)
    
    # Create directory for images
    directory = "Fetched_Images"
    if not create_directory(directory):
        print("Failed to create directory. Exiting.")
        return
    
    # Main loop
    while True:
        print("\nOptions:")
        print("1. Download an image from URL")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == '1':
            url = input("Enter the image URL: ").strip()
            
            if not url:
                print("URL cannot be empty. Please try again.")
                continue
            
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                print("Invalid URL format. URL must start with http:// or https://")
                continue
            
            # Download the image
            download_image(url, directory)
            
        elif choice == '2':
            print("Thank you for using the Image Downloader. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()