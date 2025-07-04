
    document.addEventListener('DOMContentLoaded', function () {
        const logementDetailModal = document.getElementById('logementDetailModal');
        const closeButton = logementDetailModal.querySelector('.close-button');
        const logementImageCarousel = logementDetailModal.querySelector('.logement-image-carousel');
        const logementCarouselDots = document.getElementById('logementCarouselDots');
        const addToFavForm = document.getElementById('addToFavForm');
        const addToFavBtn = addToFavForm ? addToFavForm.querySelector('.add-to-fav-btn') : null;
        const isFavorisedInput = document.getElementById('isFavorised');
        let lastFocusedElement = null;
        let currentDotIndex = 0;
        let currentLogementData = null;

        // Event Listeners for Modal
        closeButton.addEventListener('click', closeLogementModal);
        window.addEventListener('click', function (event) {
            if (event.target === logementDetailModal) {
                closeLogementModal();
            }
        });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && logementDetailModal.style.display === 'flex') {
                closeLogementModal();
            }
        });

        // Carousel Functionality
        function updateCarouselDots(activeIndex) {
            const dots = Array.from(logementCarouselDots.children);
            dots.forEach((dot, index) => {
                const isActive = index === activeIndex;
                dot.classList.toggle('active', isActive);
                dot.setAttribute('aria-selected', isActive ? 'true' : 'false');
            });
        }

        logementImageCarousel.addEventListener('scroll', function () {
            const scrollLeft = logementImageCarousel.scrollLeft;
            const itemWidth = logementImageCarousel.offsetWidth;
            if (itemWidth === 0) return;
            const newActiveIndex = Math.round(scrollLeft / itemWidth);
            if (newActiveIndex !== currentDotIndex) {
                updateCarouselDots(newActiveIndex);
                currentDotIndex = newActiveIndex;
            }
        });

        function goToImage(index) {
            const imageWrappers = logementImageCarousel.querySelectorAll('.logement-image-wrapper');
            if (imageWrappers[index]) {
                logementImageCarousel.scrollTo({
                    left: imageWrappers[index].offsetLeft,
                    behavior: 'smooth'
                });
            }
        }

      

        // Handle opening modal from "View Details" buttons
        document.body.addEventListener('click', function (event) {
            const button = event.target.closest('.view-details-btn');
            if (button) {
                lastFocusedElement = button;
                currentLogementData = {
                    id_logement: button.dataset.logementId,
                    name: button.dataset.logementName,
                    images: safelyParseJSON(button.dataset.logementImages, []),
                    type: button.dataset.logementType,
                    description: button.dataset.logementDescription,
                    rating: button.dataset.logementRating,
                    localisation: button.dataset.logementLocalisation,
                    details: safelyParseJSON(button.dataset.details, {}),
                    equipements: safelyParseJSON(button.dataset.equipement, []),
                    is_favorised: button.dataset.isFavorised === 'true'
                };
                populateLogementModal(currentLogementData);
                openLogementModal();
            }
        });

        function safelyParseJSON(jsonString, fallback) {
            try {
                return JSON.parse(jsonString || 'null') || fallback;
            } catch (e) {
                console.error("Error parsing JSON:", e, "Input:", jsonString);
                return fallback;
            }
        }

        // Modal Open/Close Functions
        function openLogementModal() {
            logementDetailModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            logementDetailModal.setAttribute('aria-hidden', 'false');
            logementDetailModal.focus();
            trapFocus(logementDetailModal);
            updateFavoriteButton(currentLogementData.is_favorised);
        }

        function closeLogementModal() {
            logementDetailModal.style.display = 'none';
            document.body.style.overflow = 'auto';
            logementDetailModal.setAttribute('aria-hidden', 'true');
            if (lastFocusedElement) {
                lastFocusedElement.focus();
                lastFocusedElement = null;
            }
        }

        // Accessibility: Focus Trap
        function trapFocus(element) {
            const focusableEls = element.querySelectorAll(
                'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
            );
            const firstFocusableEl = focusableEls[0];
            const lastFocusableEl = focusableEls[focusableEls.length - 1];
            if (!firstFocusableEl) return;
            closeButton.focus();
            element.addEventListener('keydown', function (e) {
                const isTabPressed = (e.key === 'Tab' || e.keyCode === 9);
                if (!isTabPressed) return;
                if (e.shiftKey) {
                    if (document.activeElement === firstFocusableEl) {
                        lastFocusableEl.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastFocusableEl) {
                        firstFocusableEl.focus();
                        e.preventDefault();
                    }
                }
            });
        }

        // Populate Modal Content
        function populateLogementModal(logementData) {
            document.getElementById('modalLogementName').innerText = logementData.name || 'Nom non disponible';
            document.getElementById('modalLogementRating').innerText = logementData.rating || 'N/A';
            document.getElementById('modalLogementDescription').innerText = logementData.description || 'Description non disponible.';
            document.getElementById('modalLogementLocalisation').innerText = logementData.localisation || 'Non spécifiée';
            const logementIdInput = document.getElementById('logementId');
            const reservationInput = document.getElementById('id_logement_reserver');
            if (logementIdInput) {
                logementIdInput.value = logementData.id_logement || '';
            }
            if(reservationInput){
                reservationInput.value  = logementData.id_logement || '';
            }
            const typeBadge = document.getElementById('modalLogementTypeBadge');
            if (typeBadge) typeBadge.innerText = logementData.type || 'Inconnu';

            // Populate property details
            document.getElementById('modalLogementSurface').innerText = (logementData.details.surface ? ` ${logementData.details.surface}` : 'N/A');
            document.getElementById('modalLogementPieces').innerText = logementData.details.pieces || 'N/A';
            document.getElementById('modalLogementBains').innerText = logementData.details.bains || 'N/A';
            document.getElementById('modalLogementPrix').innerText = (logementData.details.prix ? ` ${logementData.details.prix}` : 'N/A');

            // Populate images
            logementImageCarousel.innerHTML = '';
            logementCarouselDots.innerHTML = '';
            if (logementData.images && logementData.images.length > 0) {
                logementData.images.forEach((imageSrc, index) => {
                    const imgWrapper = document.createElement('div');
                    imgWrapper.classList.add('logement-image-wrapper');
                    const img = document.createElement('img');
                    img.src = imageSrc;
                    img.alt = `Image ${index + 1} of ${logementData.name}`;
                    imgWrapper.appendChild(img);
                    logementImageCarousel.appendChild(imgWrapper);

                    const dot = document.createElement('span');
                    dot.classList.add('carousel-dot');
                    dot.setAttribute('role', 'tab');
                    dot.setAttribute('aria-controls', `image-${index}`);
                    dot.setAttribute('tabindex', '0');
                    dot.addEventListener('click', () => goToImage(index));
                    logementCarouselDots.appendChild(dot);
                });
                updateCarouselDots(0);
                logementImageCarousel.scrollTo({ left: 0, behavior: 'auto' });
            } else {
                logementImageCarousel.innerHTML = '<div class="logement-image-wrapper">Aucune image disponible.</div>';
            }

            // Populate equipments
            const equipementsList = document.getElementById('modalLogementEquipements');
            const noEquipementsMessage = document.getElementById('noEquipementsMessage');
            equipementsList.innerHTML = '';
            if (logementData.equipements && logementData.equipements.length > 0) {
                logementData.equipements.forEach(equipement => {
                    const li = document.createElement('li');
                    li.textContent = equipement;
                    equipementsList.appendChild(li);
                });
                equipementsList.style.display = 'grid';
                noEquipementsMessage.style.display = 'none';
            } else {
                equipementsList.style.display = 'none';
                noEquipementsMessage.style.display = 'block';
            }

            // Update favorite button status
            updateFavoriteButton(logementData.is_favorised);
        }

        function updateFavoriteButton(isFavorited) {
            if (addToFavBtn) {
                const heartIcon = addToFavBtn.querySelector('i');
                if (isFavorited) {
                    addToFavBtn.classList.add('favorited');
                    heartIcon.classList.remove('far');
                    heartIcon.classList.add('fas');
                    addToFavBtn.textContent = ' Supprimer des favoris';
                    addToFavBtn.prepend(heartIcon);
                    isFavorisedInput.value = 'true';
                } else {
                    addToFavBtn.classList.remove('favorited');
                    heartIcon.classList.remove('fas');
                    heartIcon.classList.add('far');
                    addToFavBtn.textContent = ' Ajouter aux favoris';
                    addToFavBtn.prepend(heartIcon);
                    isFavorisedInput.value = 'false';
                }
            }
        }


       

    });
