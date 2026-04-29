fetch('/hospitals')
    .then(response => response.json())
    .then(function(hospitals) {
        var tbody = document.getElementById('tableBody');
        hospitals.forEach(function(h) {
            var row = document.createElement('tr');
            row.innerHTML = '<td>' + h.name + '</td>' +
                            '<td>' + h.address + '</td>' +
                            '<td>' + h.lat + '</td>' +
                            '<td>' + h.lng + '</td>' +
                            '<td>' + h.type + '</td>';
            tbody.appendChild(row);
        });
    });