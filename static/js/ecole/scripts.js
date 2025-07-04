
    document.addEventListener('DOMContentLoaded', function () {
        const tabButtons = document.querySelectorAll('.school-search-box .tab-button');
        tabButtons.forEach(button => {
            button.addEventListener('click', function () {
                tabButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
            });
        });


        const filterBtn = document.querySelector('.results-filter-bar .filter-btn');
        if (filterBtn) {
            filterBtn.addEventListener('click', function (event) {
            });
        }

        // --- Logique du modal ---
        const modal = document.getElementById('schoolDetailModal');
        if (!modal) {
            console.error("Modal element with ID 'schoolDetailModal' not found.");
            return;
        }

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
                const schoolName = this.dataset.schoolName;
                const schoolImages = JSON.parse(this.dataset.schoolImages);
                const schoolLocation = this.dataset.schoolLocation;
                const schoolDescription = this.dataset.schoolDescription;
                const schoolRating = this.dataset.schoolRating;
                const schoolAddress = this.dataset.schoolAddress;
                const schoolUniversity = this.dataset.schoolUniversity;

                let formations = [];
                try {
                    formations = JSON.parse(this.dataset.formations);
                } catch (e) {
                    console.error("Error parsing formations JSON:", e, this.dataset.formations);
                    formations = [];
                }

                let mapCoords = null;
                try {
                    mapCoords = JSON.parse(this.dataset.mapCoords);
                } catch (e) {
                    console.error("Error parsing mapCoords JSON:", e, this.dataset.mapCoords);
                    mapCoords = { lat: 0, lng: 0 };
                }

                const schoolData = {
                    name: schoolName,
                    images: schoolImages,
                    location: schoolLocation,
                    description: schoolDescription,
                    rating: schoolRating,
                    address: schoolAddress,
                    university: schoolUniversity,
                    formations: formations,
                    // Correction de l'URL de la carte - utilisez les backticks pour les template literals
                    mapEmbedUrl: mapCoords ? `https://maps.google.com/maps?q=${mapCoords.lat},${mapCoords.lng}&hl=fr&z=14&output=embed` : ''
                };

                populateSchoolModal(schoolData);

                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        });
    });

    function populateSchoolModal(schoolData) {
        document.getElementById('modalSchoolName').innerText = schoolData.name;
        document.getElementById('modalSchoolRating').innerText = schoolData.rating;
        document.getElementById('modalSchoolDescription').innerText = schoolData.description;
        document.getElementById('modalSchoolLocation').innerText = schoolData.location;

        const modalAddressP = document.getElementById('modalAddressP');
        const modalSchoolAddress = document.getElementById('modalSchoolAddress');
        if (schoolData.address) {
            modalSchoolAddress.innerText = schoolData.address;
            modalAddressP.style.display = 'block';
        } else {
            modalAddressP.style.display = 'none';
        }

        const modalUniversityP = document.getElementById('modalUniversityP');
        const modalSchoolUniversity = document.getElementById('modalSchoolUniversity');
        if (schoolData.university) {
            modalSchoolUniversity.innerText = schoolData.university;
            modalUniversityP.style.display = 'block';
        } else {
            modalUniversityP.style.display = 'none';
        }

        const schoolImageCarousel = document.querySelector('.school-image-carousel');
        const schoolCarouselDots = document.getElementById('schoolCarouselDots');
        schoolImageCarousel.innerHTML = '';
        schoolCarouselDots.innerHTML = '';

        if (schoolData.images && schoolData.images.length > 0) {
            schoolData.images.forEach((imgUrl, index) => {
                const imgWrapper = document.createElement('div');
                imgWrapper.classList.add('school-image-wrapper');
                imgWrapper.innerHTML = `<img src="${imgUrl}" alt="School Image ${index + 1}" class="school-image">`;
                schoolImageCarousel.appendChild(imgWrapper);

                const dot = document.createElement('span');
                dot.classList.add('carousel-dot');
                dot.dataset.index = index;
                dot.onclick = () => {
                    schoolImageCarousel.scrollTo({
                        left: imgWrapper.offsetWidth * index,
                        behavior: 'smooth'
                    });
                };
                schoolCarouselDots.appendChild(dot);
            });
            if (schoolCarouselDots.children.length > 0) {
                schoolCarouselDots.children[0].classList.add('active');
            }
        } else {
            const imgWrapper = document.createElement('div');
            imgWrapper.classList.add('school-image-wrapper');
            imgWrapper.innerHTML = `<img src="https://via.placeholder.com/960x250?text=No+Image+Available" alt="No image available" class="school-image">`;
            schoolImageCarousel.appendChild(imgWrapper);
        }

        schoolImageCarousel.removeEventListener('scroll', updateCarouselDots);
        schoolImageCarousel.addEventListener('scroll', updateCarouselDots);

        const formationsList = document.getElementById('modalFormationsList');
        formationsList.innerHTML = '';

        if (schoolData.formations && schoolData.formations.length > 0) {
            schoolData.formations.forEach(formation => {
                const formationItem = document.createElement('div');
                formationItem.classList.add('formation-item');
                formationItem.innerHTML = `
                    <div class="formation-header">
                        <h4>${formation.name}</h4>
                        <span class="degree-badge">${formation.degree}</span>
                    </div>
                    <p class="formation-description">${formation.description}</p>
                    <div class="formation-footer">
                        <span>Durée: ${formation.duration}</span>
                        <span class="formation-price">${formation.price}</span>
                    </div>
                `;
                formationsList.appendChild(formationItem);
            });
        } else {
            formationsList.innerHTML = '<p>Aucune formation disponible pour le moment.</p>';
        }

        const mapFrame = document.getElementById('modalMapFrame');
        const mapErrorOverlay = document.getElementById('mapErrorOverlay');
        if (schoolData.mapEmbedUrl) {
            mapFrame.src = schoolData.mapEmbedUrl;
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
            mapErrorOverlay.querySelector('p').innerText = 'Adresse non disponible pour la carte.';
            mapErrorOverlay.querySelector('button').style.display = 'none';
        }
    }

    function updateCarouselDots() {
        const schoolImageCarousel = document.querySelector('.school-image-carousel');
        const schoolCarouselDots = document.getElementById('schoolCarouselDots');
        if (!schoolImageCarousel || !schoolCarouselDots || schoolCarouselDots.children.length === 0) {
            return;
        }

        const scrollLeft = schoolImageCarousel.scrollLeft;
        const itemWidth = schoolImageCarousel.offsetWidth;
        const activeIndex = Math.round(scrollLeft / itemWidth);

        Array.from(schoolCarouselDots.children).forEach(dot => {
            dot.classList.remove('active');
        });

        if (schoolCarouselDots.children[activeIndex]) {
            schoolCarouselDots.children[activeIndex].classList.add('active');
        }
    }


    const favoriteButtons = document.querySelectorAll('.favorite-btn');
        favoriteButtons.forEach(button => {
            button.addEventListener('click', async function() {
                const schoolId = this.dataset.schoolId;
                const heartIcon = this.querySelector('i');
                const isCurrentlyFavorited = heartIcon.classList.contains('fas');
                updateFavoriteButton(heartIcon, !isCurrentlyFavorited);
            });
        });

        function updateFavoriteButton(iconElement, isFavorited) {
            if (isFavorited) {
                iconElement.classList.remove('far');
                iconElement.classList.add('fas');
                iconElement.style.color = '#dc3545'; 
            } else {
                iconElement.classList.remove('fas');
                iconElement.classList.add('far');
                iconElement.style.color = '#ff6b6b'; 
            }
        }
