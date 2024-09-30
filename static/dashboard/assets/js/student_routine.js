(function ($) {
    $(document).ready(function () {
        function get_format_date(today) {
            return today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
        }

        const calendarEl = document.getElementById('calendar');
        const calendar = new FullCalendar.Calendar(calendarEl, {
            headerToolbar: {
                center: 'title',
                right: 'prev,next',
                left: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            initialView: 'dayGridMonth',
            eventContent: function (info) {
                return {
                    html: info.event.title
                }
            },
            loading: function (bool) {
                console.log("Loading", bool)
            },
            selectable: true,
            selectMirror: true,
            events: function (obj, successCallback, failureCallback) {
                const start_date = get_format_date(obj.start);
                const end_date = get_format_date(obj.end);
                const section = calendarEl.getAttribute('data-section');

                const url = calendarEl.getAttribute('data-events-url');
                $.ajax({
                    url: url,
                    type: 'GET',
                    data: {
                        start_date: start_date,
                        end_date: end_date,
                        section: section
                    },
                    beforeSend: function () {
                    },
                    success: function (response) {
                        successCallback(response);
                    }
                });
            }
        });
        calendar.render();
    })
})(jQuery)