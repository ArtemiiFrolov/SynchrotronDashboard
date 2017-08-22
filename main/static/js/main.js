(function($) {
    $.fn.api.settings.cache = false;
    $.fn.api.settings.verbose = false;
    $.fn.api.settings.debug = false;

    $.fn.api.settings.api = {
        'search stations': '/api/stations/?search={query}',
        'search organizations': '/api/organizations/?search={query}',
        'search equipment': '/api/equipment/?search={query}',
        'search complete statuses': '/api/complete_statuses/?search={query}',
        'search stage statuses': '/api/stage_statuses/?search={query}',
        'search journal statuses': '/api/journal statuses/?search={query}',
        'search approaches': '/api/approaches/?search={query}',
        'search roles': '/api/approaches/?search={query}',
        'search rights': '/api/rights/?search={query}',
        'search users': '/api/users/?search={query}',
    };

    $.fn.api.settings.onResponse = function(response) {
        if (!response)
            return;

        return {
            success: response.success == undefined ? true : response.success,
            results: response,
        };
    };

    /* Dropdown settings */
    $.fn.dropdown.settings.message =  {
        addResult     : 'Добавить <b>{term}</b>',
        count         : '{count} выбрано',
        maxSelections : 'Максимум {maxCount} элементов',
        noResults     : 'Результатов не найдено'
    };
    $.fn.dropdown.settings.className.label = 'ui teal label';
    $.fn.dropdown.settings.apiSettings.cache = false;
    $.fn.dropdown.settings.saveRemoteData = false;

    /* Calendar settings */
    var add0 = function(t){return t < 10 ? '0' + t : t}
    $.fn.calendar.settings.text =  {
        days: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        months: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        monthsShort: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
        today: 'Сегодня',
        now: 'Сейчас',
        am: 'AM',
        pm: 'PM'
    };
    $.fn.calendar.settings.ampm = false;
    $.fn.calendar.settings.monthFirst = false;
    $.fn.calendar.settings.formatter.date = function(date, settings) {
        if (!date) return '';
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        return add0(day) + '.' + add0(month) + '.' + year;
    }

    /* DataTables */
    dataTablesLanguage = {
      "processing": "Подождите...",
      "search": "Поиск:",
      "lengthMenu": "Показать _MENU_ записей",
      "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
      "infoEmpty": "Записи с 0 до 0 из 0 записей",
      "infoFiltered": "(отфильтровано из _MAX_ записей)",
      "infoPostFix": "",
      "loadingRecords": "Загрузка записей...",
      "zeroRecords": "Записи отсутствуют.",
      "emptyTable": "В таблице отсутствуют данные",
      "paginate": {
        "first": "Первая",
        "previous": "Предыдущая",
        "next": "Следующая",
        "last": "Последняя"
      },
      "aria": {
        "sortAscending": ": активировать для сортировки столбца по возрастанию",
        "sortDescending": ": активировать для сортировки столбца по убыванию"
      }
    };


}(jQuery));

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$( document ).ready(function() {
     $('.search.dropdown').each(function(index) {
        var action = $(this).data('api-action');
        if(!action)
            return;
        var allowAdd = $(this).data('allow-add') != undefined;
        var multiple = $(this).attr('multiple') != undefined;
        var fieldName = $(this).data('api-field-name') || 'name';
        var fieldValue = $(this).data('api-field-value') || 'id';
        //console.log($(this), allowAdd, multiple, fieldName, fieldValue);

        $(this).dropdown({
            allowAdditions: allowAdd,
            useLabels: true,
            hideAdditions: false,
            fields: {
                name: fieldName,
                value: fieldValue,
            },
            apiSettings : {
                action: action,
            }
        });
    });

    $('.datetime').calendar({ type: 'datetime', });
    $('.enable-datatable').DataTable({
        language: dataTablesLanguage,
    });
});