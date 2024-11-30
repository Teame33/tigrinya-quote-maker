// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM elements
    const form = document.getElementById('quoteForm');
    const quoteTextInput = document.getElementById('quoteText');
    const authorInput = document.getElementById('author');
    const previewContainer = document.getElementById('quote-preview');
    const previewBackground = previewContainer.querySelector('.preview-background');
    const previewQuoteContainer = previewContainer.querySelector('.preview-quote-container');
    const previewQuoteText = previewContainer.querySelector('.preview-quote-text');
    const previewAuthor = previewContainer.querySelector('.preview-author');
    const fontFamilySelect = document.getElementById('fontFamily');
    const fontSizeSelect = document.getElementById('fontSize');
    const textColorInput = document.getElementById('textColor');
    const backgroundColorInput = document.getElementById('backgroundColor');
    const customImageInput = document.getElementById('customImage');
    const customImageSection = document.getElementById('customImageSection');
    const solidColorSection = document.getElementById('solidColorSection');
    const quoteWidthInput = document.getElementById('quoteWidth');
    const horizontalOffset = document.getElementById('horizontalOffset');
    const verticalOffset = document.getElementById('verticalOffset');
    const backgroundTypeInputs = document.querySelectorAll('input[name="backgroundType"]');
    const sizeFormatInputs = document.querySelectorAll('input[name="sizeFormat"]');
    const positionButtons = document.querySelectorAll('.position-btn');
    const saveButton = document.getElementById('saveQuote');
    const bgOpacityInput = document.getElementById('bgOpacity');
    const bgBlurInput = document.getElementById('bgBlur');

    if (!previewContainer) {
        console.error('Preview container not found');
        return;
    }

    // Show/hide background options based on type
    function toggleBackgroundOptions(type) {
        customImageSection.style.display = type === 'custom' ? 'block' : 'none';
        solidColorSection.style.display = type === 'solid' ? 'block' : 'none';
        
        // Reset text color visibility
        textColorInput.parentElement.style.display = type === 'custom' ? 'none' : 'block';
        
        if (type === 'custom') {
            // Force white text for custom backgrounds
            previewQuoteText.style.color = '#ffffff';
            previewAuthor.style.color = '#ffffff';
            // Add text shadow for better visibility
            previewQuoteText.style.textShadow = '2px 2px 4px rgba(0,0,0,0.5)';
            previewAuthor.style.textShadow = '2px 2px 4px rgba(0,0,0,0.5)';
        } else {
            previewQuoteText.style.color = textColorInput.value;
            previewAuthor.style.color = textColorInput.value;
            previewQuoteText.style.textShadow = 'none';
            previewAuthor.style.textShadow = 'none';
        }
    }

    // Update preview
    function updatePreview() {
        // Update text content
        const quoteLines = quoteTextInput.value.split('\n').filter(line => line.trim());
        previewQuoteText.innerHTML = '';
        quoteLines.forEach(line => {
            const lineDiv = document.createElement('div');
            lineDiv.className = 'quote-line';
            lineDiv.textContent = line;
            previewQuoteText.appendChild(lineDiv);
        });
        previewAuthor.textContent = authorInput.value ? `- ${authorInput.value}` : '';

        // Get selected background type
        const selectedBgType = document.querySelector('input[name="backgroundType"]:checked').value;
        if (selectedBgType === 'solid') {
            previewBackground.style.backgroundImage = 'none';
            previewBackground.style.background = backgroundColorInput.value;
            previewQuoteContainer.style.backgroundColor = 'transparent';
        } else if (selectedBgType === 'gradient') {
            previewBackground.style.backgroundImage = 'none';
            previewBackground.style.background = 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)';
            previewQuoteContainer.style.backgroundColor = 'transparent';
        } else if (selectedBgType === 'notebook') {
            previewBackground.style.background = '#f8f9fa';
            previewBackground.style.backgroundImage = 'linear-gradient(#e5e5e5 1px, transparent 1px)';
            previewBackground.style.backgroundSize = '100% 2em';
            previewQuoteContainer.style.backgroundColor = 'transparent';
        }

        // Update styles
        const styles = {
            fontFamily: fontFamilySelect.value,
            fontSize: fontSizeSelect.value + 'px',
            color: textColorInput.value,
            maxWidth: quoteWidthInput.value + '%',
            transform: `translate(${horizontalOffset.value}%, ${verticalOffset.value}%)`
        };

        Object.assign(previewQuoteText.style, styles);
        previewAuthor.style.fontFamily = styles.fontFamily;
        previewAuthor.style.color = styles.color;
    }

    // Handle background opacity
    bgOpacityInput.addEventListener('input', function() {
        const opacity = this.value / 100;
        if (previewBackground.style.backgroundImage) {
            previewQuoteContainer.style.backgroundColor = `rgba(0, 0, 0, ${1 - opacity})`;
        }
    });

    // Handle background blur
    bgBlurInput.addEventListener('input', function() {
        const blur = this.value;
        if (previewBackground.style.backgroundImage) {
            previewBackground.style.filter = `blur(${blur}px)`;
        }
    });

    // Handle custom image upload
    customImageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const imageUrl = event.target.result;
                previewBackground.style.backgroundImage = `url('${imageUrl}')`;
                previewBackground.style.backgroundSize = 'cover';
                previewBackground.style.backgroundPosition = 'center';
                previewQuoteContainer.style.backgroundColor = `rgba(0, 0, 0, ${1 - bgOpacityInput.value/100})`;
                previewBackground.style.filter = `blur(${bgBlurInput.value}px)`;
                previewContainer.classList.add('custom-bg');
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle size format changes
    sizeFormatInputs.forEach(input => {
        input.addEventListener('change', function() {
            const format = this.value;
            if (format === 'instagram') {
                previewContainer.style.aspectRatio = '1/1';
            } else if (format === 'facebook') {
                previewContainer.style.aspectRatio = '16/9';
            } else if (format === 'tiktok') {
                previewContainer.style.aspectRatio = '9/16';
            }
            updatePreview();
        });
    });

    // Event listeners
    quoteTextInput.addEventListener('input', updatePreview);
    authorInput.addEventListener('input', updatePreview);
    fontFamilySelect.addEventListener('change', updatePreview);
    fontSizeSelect.addEventListener('change', updatePreview);
    textColorInput.addEventListener('input', updatePreview);
    backgroundColorInput.addEventListener('input', updatePreview);
    quoteWidthInput.addEventListener('input', updatePreview);
    horizontalOffset.addEventListener('input', updatePreview);
    verticalOffset.addEventListener('input', updatePreview);

    backgroundTypeInputs.forEach(input => {
        input.addEventListener('change', function() {
            toggleBackgroundOptions(this.value);
            updatePreview();
        });
    });

    positionButtons.forEach(button => {
        button.addEventListener('click', () => {
            positionButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            updatePreview();
        });
    });

    // Initial update
    toggleBackgroundOptions('solid');
    updatePreview();

    // Save quote functionality
    saveButton?.addEventListener('click', async function() {
        try {
            // Hide the download button temporarily while generating image
            saveButton.disabled = true;
            saveButton.textContent = 'Generating...';

            // Use html2canvas to capture the preview
            const canvas = await html2canvas(previewContainer, {
                scale: 2, // Higher quality
                useCORS: true,
                allowTaint: true,
                backgroundColor: null
            });

            // Convert to blob
            canvas.toBlob(function(blob) {
                // Create download link
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'quote.png';

                // Trigger download
                document.body.appendChild(a);
                a.click();

                // Cleanup
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // Reset button
                saveButton.disabled = false;
                saveButton.textContent = 'Save Quote';
            }, 'image/png');

        } catch (error) {
            console.error('Error saving quote:', error);
            saveButton.disabled = false;
            saveButton.textContent = 'Save Quote';
            alert('Error saving quote. Please try again.');
        }
    });
});