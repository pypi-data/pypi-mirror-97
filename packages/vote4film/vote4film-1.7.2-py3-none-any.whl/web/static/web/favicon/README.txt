# Instructions

Background Colour: #4d394b

1. Go to https://realfavicongenerator.net/
2. Use projector.svg
3. Favicon for Desktop Browsers
    a. Select add margins and plain background
    b. Set background color
    c. Set background radius to 5
    d. Set image size to maximum
4. Favicon for iOS
    a. Select add a solid, plain background
    b. Set margin size to 0
    c. Check create all icons for iOS 7 and later
    d. Uncheck in the HTML, declare only the icon with highest resolution
5. Favicon for Android Chrome
    a. Set solid, plain background
    b. Set background colour
    c. Set margin size to 0
    d. Set app name
    e. Set theme colour
    f. Select standalone mode
    g. Set start URL
    h. Check create all documented icons
6. Windows Metro
    a. Set background colour
    b. Windows 8.1+, generate all icon sizes
7. macOS Safari
    a. Set theme colour
8. Favicon Generator Options
    a. Set favicon path "/web/favicon"
    b. Set this website is already in production
    c. Set compression
    d. Set app name


Then, download:

1. Place into this folder (delete everything except README.txt and projector.svg)
2. Modify the HTML to add the Django {% static %} tags
3. Simply icon names to match favicon.ico naming
4. TODO: HACK: Modify browserconfig.xml to add "/static"
5. Merge site.webmanifest with manifest.webmanifest


TODO:

1. Modify icon to fit mask https://web.dev/maskable-icon/
