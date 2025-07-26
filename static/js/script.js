document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('category');
    const cropSelect = document.getElementById('crop');
    const stateSelect = document.getElementById('state');
    const districtSelect = document.getElementById('district');

    // Handle category change
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const category = this.value;
            cropSelect.innerHTML = '<option value="">Select Crop</option>';
            
            if (category) {
                fetch(`/get_crops/${category}`)
                    .then(response => response.json())
                    .then(crops => {
                        crops.forEach(crop => {
                            const option = document.createElement('option');
                            option.value = crop;
                            option.textContent = crop;
                            cropSelect.appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching crops:', error);
                    });
            }
        });
    }

    // Handle state change
    if (stateSelect) {
        stateSelect.addEventListener('change', function() {
            const state = this.value;
            districtSelect.innerHTML = '<option value="">Select District</option><option value="Others">Others (if district not available)</option>';
            
            if (state) {
                fetch(`/get_districts/${state}`)
                    .then(response => response.json())
                    .then(districts => {
                        districts.forEach(district => {
                            if (district !== 'Others') {
                                const option = document.createElement('option');
                                option.value = district;
                                option.textContent = district;
                                districtSelect.appendChild(option);
                            }
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching districts:', error);
                    });
            }
        });
    }

    // Form validation
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(e) {
            const requiredFields = ['category', 'crop', 'state', 'district', 'month'];
            let isValid = true;

            requiredFields.forEach(fieldName => {
                const field = document.getElementById(fieldName);
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    }

    // Set default month to current month
    const monthInput = document.getElementById('month');
    if (monthInput) {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        monthInput.value = `${year}-${month}`;
    }
});
