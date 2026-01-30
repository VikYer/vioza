document.addEventListener('DOMContentLoaded', function () {

    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');
    const regionSelect = document.getElementById('id_region');
    const citySelect = document.getElementById('id_city');

    if (categorySelect && subcategorySelect) {
        categorySelect.addEventListener('change', function () {
            const categoryId = this.value;
            subcategorySelect.innerHTML = '<option value="">---------</option>';

            if (!categoryId) return;

            fetch(`/ajax/subcategories/${categoryId}/`)
                .then(res => res.json())
                .then(data => {
                    data.subcategories.forEach(sub => {
                        const option = document.createElement('option');
                        option.value = sub.slug;
                        option.textContent = sub.title;
                        subcategorySelect.appendChild(option);
                    });
                });
        });
    }

    if (regionSelect && citySelect) {
        regionSelect.addEventListener('change', function () {
            const regionId = this.value;
            citySelect.innerHTML = '<option value="">---------</option>';

            if (!regionId) return;

            fetch(`/ajax/cities/${regionId}/`)
                .then(res => res.json())
                .then(data => {
                    data.cities.forEach(city => {
                        const option = document.createElement('option');
                        option.value = city.id;
                        option.textContent = city.name;
                        citySelect.appendChild(option);
                    });
                });
        });
    }

});