(function () {
    $(document).ready(function () {

        function get_format_date(today) {
            return today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
        }

        const addRoutineModal = $(document).find("#addRoutineModal");
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
                console.log("Events", obj)
                const start_date = get_format_date(obj.start);
                const end_date = get_format_date(obj.end);

                const url = calendarEl.getAttribute('data-events-url');
                $.ajax({
                    url: url,
                    type: 'GET',
                    data: {
                        start_date: start_date,
                        end_date: end_date
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

        calendar.on('dateClick', function (info) {
            const clickedDate = info.date;
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (clickedDate < today) {
                alert("You cannot select a past date.");
                return;
            }

            const format_date = get_format_date(info.date);
            addRoutineModal.find("[name=date]").val(format_date).trigger("change")
            addRoutineModal.modal("show");
        });

        $(document).on("submit", "#addRoutineModal form", function (e) {
            e.preventDefault();
            const form = $(this);
            const url = form.attr("action");
            const btn = form.find("button[type=submit]");

            $.ajax({
                url: url,
                type: 'POST',
                data: form.serialize(),
                beforeSend: function () {
                    btn.attr("disabled", false).html("Adding routine...");
                },
                success: function (response) {
                    calendar.refetchEvents();
                    addRoutineModal.modal("hide");
                },
                error: function (response) {
                    alert("Unable to add routine");
                },
                complete: function () {
                    btn.attr("disabled", false).html("Add routine");
                }
            });
        })
    })
})(jQuery)