let deleteButtons = document.querySelectorAll('.delete_note')

deleteButtons.forEach(function(button){

    button.addEventListener('click', function(ev){

        let confirmDelete = confirm("Are you sure you would like to delete this note?");

        if(!confirmDelete) {
            ev.preventDefault();
        }

    })
});