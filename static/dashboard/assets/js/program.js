function fetchdepartment() {
    const campusId = document.getElementById('campus-select').value;

    // Correct the template literal syntax and URL path
    fetch(`/department/${campusId}`)
        .then(response => response.json())
        .then(data => {
            const departmentSelect = document.getElementById('department-select');
            
            // Clear existing options
            departmentSelect.innerHTML = '<option value="" disabled selected>Select a department</option>';

            // Populate new options
            data.forEach(department => {
                const option = document.createElement('option');
                option.value = department.id;
                option.textContent = department.name;
                departmentSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching department:', error));
}