document.addEventListener('DOMContentLoaded', function () {

        const cards = document.querySelectorAll('.category-card');
        const container = document.getElementById('subcategory-container');
        const row = document.getElementById('subcategory-row');
        const title = document.getElementById('subcategory-title');

        let activeCategory = null;

        cards.forEach(card => {
            card.addEventListener('click', (event) => {
                // Prevent click from bubbling to document
                event.stopPropagation();

                const categoryId = card.dataset.categoryId;
                const categoryTitle = card.dataset.categoryTitle;
                const categorySlug = card.dataset.categorySlug;

                // Toggle: close if the same category is clicked again
                if (activeCategory === categoryId) {
                    closePanel();
                    return;
                }

                activeCategory = categoryId;

                fetch(`/ajax/subcategories/${categoryId}/`)
                    .then(response => response.json())
                    .then(data => {

                        row.innerHTML = '';


                        // Category title as a link
                        title.innerHTML = `
                            <a href="/ads/${categorySlug}/"class="text-decoration-none">
                                All in ${categoryTitle}
                            </a>
                        `;

                        // Subcategories grid
                        data.subcategories.forEach(sub => {
                            row.innerHTML += `
                                <div class="col-md-4 col-lg-3 mb-2">
                                    <a href="/ads/${categorySlug}/${sub.slug}/" class="list-group-item">
                                        ${sub.title}
                                    </a>
                                </div>
                            `;
                        });

                        container.classList.remove('d-none');
                        container.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    });
            });
        });

        // Click outside categories or subcategory panel closes the panel
        document.addEventListener('click', (event) => {
            if (
                !container.contains(event.target) &&
                !event.target.closest('.category-card')
            ) {
                closePanel();
            }
        });

        function closePanel() {
            container.classList.add('d-none');
            row.innerHTML = '';
            activeCategory = null;
        }

    });