   document.addEventListener('DOMContentLoaded', function () {
        const modal = document.getElementById('logementDetailModal');
        const closeButton = modal.querySelector('.close-button');
        if (closeButton) {
            closeButton.addEventListener('click', function () {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            });
        } else {
            console.warn("Close button not found within the modal.");
        }

        window.addEventListener('click', function (event) {
            if (event.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });

        const viewDetailsButtons = document.querySelectorAll('.view-details-btn');

        viewDetailsButtons.forEach(button => {
            button.addEventListener('click', function () {
                const logementId = this.dataset.logementId;
                const logementName = this.dataset.logementName;
                const logementImages = JSON.parse(this.dataset.logementImages);
                const logementLocation = this.dataset.logementLocalisation; 
                const logementDescription = this.dataset.logementDescription;
                const logementRating = this.dataset.logementRating;
                const logementType = this.dataset.logementType;
                const logementDetails = JSON.parse(this.dataset.details); 
                const logementEquipement = JSON.parse(this.dataset.equipement); 
                const isFavorised = this.dataset.isFavorised === 'true'; 
                let mapCoords = null;
                const logementData = {
                    id: logementId,
                    name: logementName,
                    images: logementImages,
                    location: logementLocation,
                    description: logementDescription,
                    rating: logementRating,
                    type: logementType,
                    details: logementDetails, 
                    equipement: logementEquipement,
                    isFavorised: isFavorised,
                };

                populateLogementModal(logementData);

                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        });

        const favoriteButtons = document.querySelectorAll('.favorite-btn');
        favoriteButtons.forEach(button => {
            button.addEventListener('click', async function() {
                const logementId = this.dataset.logementId;
                const heartIcon = this.querySelector('i');
                const isCurrentlyFavorited = heartIcon.classList.contains('fas');
                updateFavoriteButton(heartIcon, !isCurrentlyFavorited);
            });
        });

        function updateFavoriteButton(iconElement, isFavorited) {
            if (isFavorited) {
                iconElement.classList.remove('far');
                iconElement.classList.add('fas');
                
            } else {
                iconElement.classList.remove('fas');
                iconElement.classList.add('far');
                
            }
        }

   
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

    });

    function populateLogementModal(logementData) {
        document.getElementById('modalLogementName').innerText = logementData.name;
        document.getElementById('modalLogementRating').innerText = logementData.rating;
        document.getElementById('modalLogementDescription').innerText = logementData.description;
        document.getElementById('modalLogementLocation').innerText = logementData.location;

       
        const modalFavoriteButton = document.getElementById('modalLogementFavoriteBtn');
        if (modalFavoriteButton) {
            modalFavoriteButton.dataset.logementId = logementData.id;
            const icon = modalFavoriteButton.querySelector('i');
            if (logementData.isFavorised) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                icon.style.color = '#dc3545';
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                icon.style.color = '#ff6b6b';
            }
        }


        // Update carousel images
        const logementImageCarousel = document.querySelector('.logement-image-carousel'); // Changed selector
        const logementCarouselDots = document.getElementById('logementCarouselDots'); // Changed ID
        logementImageCarousel.innerHTML = '';
        logementCarouselDots.innerHTML = '';

        if (logementData.images && logementData.images.length > 0) {
            logementData.images.forEach((imgUrl, index) => {
                const imgWrapper = document.createElement('div');
                imgWrapper.classList.add('logement-image-wrapper'); // Changed class
                imgWrapper.innerHTML = `<img src="${imgUrl}" alt="Logement Image ${index + 1}" class="logement-image">`; // Changed alt and class
                logementImageCarousel.appendChild(imgWrapper);

                const dot = document.createElement('span');
                dot.classList.add('carousel-dot');
                dot.dataset.index = index;
                dot.onclick = () => {
                    logementImageCarousel.scrollTo({
                        left: imgWrapper.offsetWidth * index,
                        behavior: 'smooth'
                    });
                };
                logementCarouselDots.appendChild(dot);
            });
            if (logementCarouselDots.children.length > 0) {
                logementCarouselDots.children[0].classList.add('active');
            }
        } else {
            const imgWrapper = document.createElement('div');
            imgWrapper.classList.add('logement-image-wrapper');
            imgWrapper.innerHTML = `<img src="https://via.placeholder.com/960x250?text=No+Image+Available" alt="No image available" class="logement-image">`;
            logementImageCarousel.appendChild(imgWrapper);
        }

        logementImageCarousel.removeEventListener('scroll', updateCarouselDots);
        logementImageCarousel.addEventListener('scroll', updateCarouselDots);

        // Update details list (surface, rooms, bathrooms, price)
        const modalLogementDetailsList = document.getElementById('modalLogementDetailsList');
        modalLogementDetailsList.innerHTML = '';
        if (logementData.details) {
            for (const key in logementData.details) {
                if (logementData.details.hasOwnProperty(key)) {
                    const listItem = document.createElement('li');
                    let iconClass = '';
                    let label = '';
                    switch (key) {
                        case 'surface':
                            iconClass = 'fas fa-ruler-combined';
                            label = 'Surface:';
                            break;
                        case 'pieces':
                            iconClass = 'fas fa-bed';
                            label = 'Chambres:';
                            break;
                        case 'bains':
                            iconClass = 'fas fa-bath';
                            label = 'Salles de bain:';
                            break;
                        case 'prix':
                            iconClass = 'fas fa-euro-sign'; // Or appropriate currency icon
                            label = 'Prix:';
                            break;
                        default:
                            break;
                    }
                    listItem.innerHTML = `<i class="${iconClass}"></i> ${label} <span>${logementData.details[key]}</span>`;
                    modalLogementDetailsList.appendChild(listItem);
                }
            }
        } else {
             modalLogementDetailsList.innerHTML = '<p>Aucun détail disponible.</p>';
        }


        // Update amenities/equipment
        const modalLogementAmenitiesList = document.getElementById('modalLogementAmenitiesList');
        modalLogementAmenitiesList.innerHTML = '';
        if (logementData.equipement && logementData.equipement.length > 0) {
            logementData.equipement.forEach(amenity => {
                const amenityTag = document.createElement('span');
                amenityTag.classList.add('amenity-tag');
                amenityTag.innerText = amenity;
                modalLogementAmenitiesList.appendChild(amenityTag);
            });
        } else {
            modalLogementAmenitiesList.innerHTML = '<span class="amenity-tag">Aucun équipement disponible.</span>';
        }


        // Map section (if applicable for housing)
        // Ensure you have elements with IDs 'modalMapFrame' and 'mapErrorOverlay' in your details.html
        const mapFrame = document.getElementById('modalMapFrame');
        const mapErrorOverlay = document.getElementById('mapErrorOverlay');
        if (mapFrame && mapErrorOverlay) {
            const mapEmbedUrl = logementData.mapEmbedUrl || ''; // If you add mapEmbedUrl to logementData

            if (mapEmbedUrl) {
                mapFrame.src = mapEmbedUrl;
                mapFrame.onload = function () {
                    try {
                        const iframeDoc = mapFrame.contentDocument || mapFrame.contentWindow.document;
                        mapErrorOverlay.style.display = 'none';
                    } catch (e) {
                        console.warn("Could not access iframe content directly due to same-origin policy, showing error overlay as fallback.", e);
                        mapErrorOverlay.style.display = 'flex';
                    }
                };
                mapFrame.onerror = function () {
                    console.error("Error loading map iframe.");
                    mapErrorOverlay.style.display = 'flex';
                };
                mapErrorOverlay.style.display = 'none';
                mapErrorOverlay.querySelector('p').innerText = 'Impossible de charger Google Maps correctement sur cette page.';
                mapErrorOverlay.querySelector('button').style.display = 'inline-block';
            } else {
                mapFrame.src = '';
                mapErrorOverlay.style.display = 'flex';
                mapErrorOverlay.querySelector('p').innerText = 'Localisation non disponible pour la carte.';
                mapErrorOverlay.querySelector('button').style.display = 'none';
            }
        }
    }

    function updateCarouselDots() {
        const logementImageCarousel = document.querySelector('.logement-image-carousel');
        const logementCarouselDots = document.getElementById('logementCarouselDots');
        if (!logementImageCarousel || !logementCarouselDots || logementCarouselDots.children.length === 0) {
            return;
        }

        const scrollLeft = logementImageCarousel.scrollLeft;
        const itemWidth = logementImageCarousel.offsetWidth;
        const activeIndex = Math.round(scrollLeft / itemWidth);

        Array.from(logementCarouselDots.children).forEach(dot => {
            dot.classList.remove('active');
        });

        if (logementCarouselDots.children[activeIndex]) {
            logementCarouselDots.children[activeIndex].classList.add('active');
        }
    }

    document.addEventListener('logementFavorited', function(e) { 
        const { logementId, isFavorited } = e.detail;
        const cardFavoriteButton = document.querySelector(`.housing-card [data-logement-id="${logementId}"]`); // Corrected selector
        if (cardFavoriteButton) {
            const favIcon = cardFavoriteButton.querySelector('i');
            if (favIcon) {
                if (isFavorited) {
                    favIcon.classList.remove('far');
                    favIcon.classList.add('fas');
                    favIcon.style.color = '#dc3545'; 
                } else {
                    favIcon.classList.remove('fas');
                    favIcon.classList.add('far');
                    favIcon.style.color = '#ff6b6b'; 
                }
            }
            const viewDetailsBtn = cardFavoriteButton.closest('.housing-card').querySelector('.view-details-btn');
            if (viewDetailsBtn) {
                viewDetailsBtn.dataset.isFavorised = isFavorited;
            }
        }
    });
