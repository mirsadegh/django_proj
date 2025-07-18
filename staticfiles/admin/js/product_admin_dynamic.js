(function($) {
    $(document).ready(function() {
        var $categorySelect = $('#id_category');
        var $productSpecificationInlines = $('.inline-related.tabular');

        function updateSpecificationChoices(categoryId) {
            var specifications = window.categorySpecifications[categoryId] || [];
            
            $productSpecificationInlines.find('.form-row.field-specification select').each(function() {
                var $specSelect = $(this);
                var currentVal = $specSelect.val();
                $specSelect.empty();
                $specSelect.append($('<option></option>').attr('value', '').text('---------')); // Add empty option
                
                $.each(specifications, function(i, spec) {
                    $specSelect.append($('<option></option>').attr('value', spec.id).text(spec.name));
                });
                
                // Try to re-select the current value if it's still valid
                if (currentVal && specifications.some(spec => spec.id == currentVal)) {
                    $specSelect.val(currentVal);
                }
            });
        }

        // Initial call on page load
        var initialCategoryId = $categorySelect.val();
        if (initialCategoryId) {
            updateSpecificationChoices(initialCategoryId);
        }

        // Bind change event
        $categorySelect.change(function() {
            var selectedCategoryId = $(this).val();
            updateSpecificationChoices(selectedCategoryId);
        });

        // Handle "Add another Product specification" button
        // This ensures new inline forms also get updated choices
        $productSpecificationInlines.on('click', '.add-row a', function() {
            // Give Django's dynamic formset a moment to add the new row
            setTimeout(function() {
                var selectedCategoryId = $categorySelect.val();
                if (selectedCategoryId) {
                    updateSpecificationChoices(selectedCategoryId);
                }
            }, 100); 
        });
    });
})(django.jQuery);
