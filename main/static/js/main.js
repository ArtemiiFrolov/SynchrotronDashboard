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

}(jQuery));