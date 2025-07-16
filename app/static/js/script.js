document.addEventListener('DOMContentLoaded', () => {
    // Set the current date in the header
    const dateElement = document.querySelector('.card-header p');
    if (dateElement) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = new Date().toLocaleDateString('en-US', options);
    }

    // Add a confirmation dialog for all delete buttons
    const deleteButtons = document.querySelectorAll('.task-delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Prevent the link from being followed immediately
            event.preventDefault(); 
            
            const userConfirmed = confirm('Are you sure you want to delete this task?');
            
            if (userConfirmed) {
                // If confirmed, navigate to the delete link
                window.location.href = this.href;
            }
            // If not confirmed, do nothing
        });
    });

    console.log('Professional To-Do App UI is ready!');
});
