document.getElementById('resultAddMoreFields').addEventListener('click', function() {
    // Get the table body
    var tableBody = document.querySelector('#subjectsTable tbody');
    
    // Clone the first row
    var newRow = tableBody.querySelector('tr').cloneNode(true);
    
    // Reset input values in the cloned row
    newRow.querySelectorAll('input').forEach(function(input) {
      input.value = ''; 
    });
    
    // Append the new row to the table
    tableBody.appendChild(newRow);
  });