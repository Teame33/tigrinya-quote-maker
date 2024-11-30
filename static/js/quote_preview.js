// Quote Preview Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Existing elements
    const quoteText = document.getElementById('quoteText');
    const author = document.getElementById('author');
    const previewQuote = document.getElementById('previewQuote');
    const previewAuthor = document.getElementById('previewAuthor');
    const fontSelect = document.getElementById('fontFamily');
    const fontSize = document.getElementById('fontSize');
    const textColor = document.getElementById('textColor');
    const backgroundColor = document.getElementById('backgroundColor');
    const gradientStart = document.getElementById('gradientStart');
    const gradientEnd = document.getElementById('gradientEnd');
    const bgTypeInputs = document.getElementsByName('backgroundType');
    const quoteContainer = document.querySelector('.quote-preview');

    // Logo elements
    const showTopLogo = document.getElementById('showTopLogo');
    const showBottomLogo = document.getElementById('showBottomLogo');
    const logoSize = document.getElementById('logoSize');
    const logoSizeValue = document.getElementById('logoSizeValue');
    const customLogo = document.getElementById('customLogo');
    const topLogo = document.querySelector('.preview-logo-top');
    const bottomLogo = document.querySelector('.preview-logo-bottom');

    // Update logo visibility
    const updateLogoVisibility = () => {
        if (topLogo) {
            topLogo.classList.toggle('hidden', !showTopLogo.checked);
        }
        if (bottomLogo) {
            bottomLogo.classList.toggle('hidden', !showBottomLogo.checked);
        }
    };

    // Update logo size
    const updateLogoSize = () => {
        const size = logoSize.value;
        logoSizeValue.textContent = size;
        document.querySelectorAll('.preview-logo img').forEach(logo => {
            logo.style.maxWidth = `${size}px`;
        });
    };

    // Handle custom logo upload
    const handleCustomLogo = (e) => {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.querySelectorAll('.preview-logo').forEach(logo => {
                    logo.classList.add('has-logo');
                    logo.querySelector('img').src = e.target.result;
                });
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    };

    // Update preview on any input change
    const updatePreview = () => {
        // Update quote text and author
        previewQuote.textContent = quoteText.value || 'Your quote will appear here';
        previewAuthor.textContent = author.value ? `- ${author.value}` : '';

        // Apply font family
        previewQuote.style.fontFamily = fontSelect.value;
        previewAuthor.style.fontFamily = fontSelect.value;

        // Apply font size
        previewQuote.style.fontSize = `${fontSize.value}px`;
        previewAuthor.style.fontSize = `${Math.max(14, fontSize.value * 0.7)}px`;

        // Apply text color
        previewQuote.style.color = textColor.value;
        previewAuthor.style.color = textColor.value;

        // Apply background based on selected type
        const selectedBgType = Array.from(bgTypeInputs).find(input => input.checked).value;
        
        // Reset background properties
        quoteContainer.style.background = '';
        quoteContainer.style.backgroundImage = '';
        quoteContainer.style.backgroundSize = '';
        quoteContainer.style.backgroundPosition = '';
        quoteContainer.style.backgroundRepeat = '';
        
        switch(selectedBgType) {
            case 'solid':
                quoteContainer.style.background = backgroundColor.value;
                break;
            case 'gradient':
                quoteContainer.style.background = `linear-gradient(135deg, ${gradientStart.value}, ${gradientEnd.value})`;
                break;
            case 'notebook':
                quoteContainer.style.background = '#ffffff';
                quoteContainer.style.backgroundImage = `
                    linear-gradient(#e1e1e1 1px, transparent 1px)
                `;
                quoteContainer.style.backgroundSize = '100% 2rem';
                quoteContainer.style.backgroundPosition = '0 1.2rem';
                break;
            case 'custom':
                // Custom image handling remains in the file input event listener
                break;
        }
    };

    // Add event listeners to all input elements
    [quoteText, author, fontSelect, fontSize, textColor, backgroundColor, 
     gradientStart, gradientEnd].forEach(element => {
        if (element) {
            element.addEventListener('input', updatePreview);
        }
    });

    bgTypeInputs.forEach(input => {
        input.addEventListener('change', () => {
            // Toggle visibility of relevant options
            document.getElementById('solidColorPicker').classList.toggle('d-none', input.value !== 'solid');
            document.getElementById('gradientColorPicker').classList.toggle('d-none', input.value !== 'gradient');
            document.getElementById('customImageUpload').classList.toggle('d-none', input.value !== 'custom');
            updatePreview();
        });
    });

    // Handle custom image upload
    const backgroundImage = document.getElementById('backgroundImage');
    if (backgroundImage) {
        backgroundImage.addEventListener('change', function(e) {
            if (e.target.files && e.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    quoteContainer.style.backgroundImage = `url(${e.target.result})`;
                    quoteContainer.style.backgroundSize = 'cover';
                    quoteContainer.style.backgroundPosition = 'center';
                };
                reader.readAsDataURL(e.target.files[0]);
            }
        });
    }

    // Add logo event listeners
    if (showTopLogo) showTopLogo.addEventListener('change', updateLogoVisibility);
    if (showBottomLogo) showBottomLogo.addEventListener('change', updateLogoVisibility);
    if (logoSize) {
        logoSize.addEventListener('input', updateLogoSize);
        logoSize.addEventListener('input', () => {
            logoSizeValue.textContent = logoSize.value;
        });
    }
    if (customLogo) customLogo.addEventListener('change', handleCustomLogo);

    // Initial updates
    updatePreview();
    updateLogoVisibility();
    updateLogoSize();
});
