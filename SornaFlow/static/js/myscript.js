// employee_panel-------------------------------------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.task-card form').forEach(form => {
        const statusButtons = form.querySelectorAll('.status-buttons button');
        const hiddenStatusInput = form.querySelector('input[name="status"]');

        statusButtons.forEach(button => {
            button.addEventListener('click', function() {

                const statusValue = this.dataset.status; 

                hiddenStatusInput.value = statusValue;
                statusButtons.forEach(btn => btn.classList.remove('selected'));
                this.classList.add('selected');
            });
        });

        form.addEventListener('submit', function(event) {
            if (hiddenStatusInput.value === "") {
                alert('لطفاً وضعیت وظیفه را انتخاب کنید.');
                event.preventDefault();
            }
        });
    });
});