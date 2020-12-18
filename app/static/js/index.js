for (let i = 0; i < 5; i++) {
    callTable(i)
}

function callTable(i) {
    setTimeout(function() {
        $table.bootstrapTable();
        console.log('Table called time #' + i);
    }, 2000 * i);
}

    // <!-- Get column options -->
    var colOptions;
    
    function getColumnNames() {
        console.log("IN GET COLUMNS")
        // console.log(params)
        var request = new XMLHttpRequest();
        // request.open('GET', '/header_options', false);  // `false` makes the request synchronous
        request.open('GET', '/data/column_options.json', false);  // `false` makes the request synchronous
        request.send(null);

        if (request.status === 200) {
            colOptions = JSON.parse(request.responseText);
            console.log("GOT THEM...")
        }
        console.log("Got column names.")
    }
    getColumnNames()


    // <!-- Reset button -->
    var $table = $('#table')
    var $resetButton = $('#resetButton')
    

    // <!-- Get data -->
    var requestCount = 0
    var initial_state = true
    var requestParams
    var initialSortColumn
    var initialFilterColumn = 'state'
    var initialFilterValue = 'AK'
    var initialStateAddition

    var page = window.location.href.split('//')[1].split('/')[1]

    console.log("COUNT REQUEST RESET TO 0")
    function ajaxRequest(params) {
        console.log(params)
        console.log("THOSE WERE THE PARAMS")
        if(page.includes('data-150k-and-up')) {
            initialSortColumn = 'loanrange'
        } else if(page.includes('data-under-150k')) {
            initialSortColumn = 'loanamount'
        }

        $('select[class*="bootstrap-table-filter-control-state"]').each(function(i) {
            if ($(this).children('option[selected="selected"]').length != 0) {
                // alert($(this).children('option[selected="selected"]').attr('value'));
                console.log('there\'s a state!')
                // console.log($(this).children('option[selected="selected"]').attr('value'))
                // console.log(initialFilterValue)
                // console.log(($(this).children('option[selected="selected"]').attr('value') != initialFilterValue))
                if ($(this).children('option[selected="selected"]').attr('value') != initialFilterValue) {
                    initial_state = false;
                    console.log('Initial state set to false because a new state is chosen.');
                }
            } else {
                initial_state = false;
                console.log('Initial state is false because no state is chosen.')
            }
        });
        console.log('Request Count: ' + requestCount)
        var url = '/data'
        console.log("HERE ARE THE PARAMS IN THE REQUEST:")
        console.log($.param(params.data))
        console.log("END PARAMS")
        // $.get(url + '?' + $.param(params.data))

        if (requestCount == 0) {
            requestParams = 'search=&sort='
                            + initialSortColumn
                            + '&order=asc&offset=0&limit=10&filter=%7B%22'
                            + initialFilterColumn
                            + '%22%3A%22'
                            + initialFilterValue
                            + '%22%7D'
            console.log("Manual params:")
            console.log(requestParams)
        } else {
            if (initial_state){
                console.log('STILL INITIAL STATE')
                console.log($.param(params.data))
                console.log($.param(params.data).includes('filter'))
                if ($.param(params.data).includes('filter')){
                    initialStateAddition = '%2C%22' + initialFilterColumn + '%22%3A%22' + initialFilterValue + '%22'
                    requestParams = $.param(params.data).substring(0, $.param(params.data).length - 3) + initialStateAddition + $.param(params.data).substring($.param(params.data).length - 3, $.param(params.data).length);
                } else {
                    initialStateAddition = '&filter=%7B%22' + initialFilterColumn + '%22%3A%22' + initialFilterValue + '%22%7D'
                    requestParams = $.param(params.data) + initialStateAddition;
                }
            } else {
            console.log('NOT INITIAL STATE ANYMORE')
            requestParams = $.param(params.data)
            }
        }
        console.log('The request params are: \r\n' + requestParams)
        console.log(url + '?' + 'page=' + page + '&' + requestParams)
        $.get(url + '?' + 'page=' + page + '&' + requestParams)
        
        .then(function (res) {
            params.success(res)
            console.log(res)
        });
        requestCount++;
    };
    

    // <!-- Format loan amount data -->        
    
        function amountFormatter(value) {
            // return value.substring(0, value.length - 3)
            return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    
        function naicsFormatter(value) {
            if (colOptions["naicscode"][value]) {
                return colOptions["naicscode"][value].replace(' ', '<br>');
            } else {
                return "N/A";
            }
        }

    // <!-- Custom text for loading message, footer, search box placeholder, no match found -->
            
        (function ($) {
            'use strict';
            $.fn.bootstrapTable.locales['en-US-custom'] = {
                formatLoadingMessage: function () {
                    return 'Doing government work';
                },
                formatRecordsPerPage: function (pageNumber) {
                    return pageNumber + ' results per page';
                },
                formatShowingRows: function (pageFrom, pageTo, totalRows) {
                    return 'Showing ' + pageFrom.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' to ' + pageTo.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' of ' + totalRows.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' loans';
                },
                formatSearch: function () {
                    return 'Search all columns';
                },
                formatNoMatches: function () {
                    return '<br>There are no loans in the center of that particular Venn diagram...<br><br>¯\\_(ツ)_/¯<br><br>but don\'t give up! Try it again with fewer filters.<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>';
                },
                formatExport: function () {
                    return 'Export page'
                }
            };
            $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['en-US-custom']);
        })(jQuery);
    

    // <!-- Format data when a row is expanded -->

        var orderedData
        function getOrderedData() {
            if(page.includes('data-150k-and-up')) {
                orderedData = {
                    "loanrange": "Loan Range",
                    "businessname": "Business Name",
                    "address": "Address",
                    "city": "City",
                    "state": "State",
                    "zip": "ZIP Code",
                    "naicscode": "Industry (NAICS Code)",
                    "businesstype": "Business Type",
                    "raceethnicity": "Race/Ethnicity",
                    "gender": "Gender",
                    "veteran": "Veteran",
                    "nonprofit": "Nonprofit",
                    "jobsreported": "Jobs Reported",
                    "dateapproved": "Date Approved",
                    "lender": "Lender",
                    "cd": "House District"
                }
            } else if(page.includes('data-under-150k')) {
                orderedData = {
                    "loanamount": "Loan Amount",
                    "city": "City",
                    "state": "State",                
                    "zip": "ZIP Code",
                    "naicscode": "Industry (NAICS Code)",
                    "businesstype": "Business Type",
                    "raceethnicity": "Race/Ethnicity",
                    "gender": "Gender",
                    "veteran": "Veteran",
                    "nonprofit": "Nonprofit",
                    "jobsreported": "Jobs Reported",
                    "dateapproved": "Date Approved",
                    "lender": "Lender",
                    "cd": "House District"
                }
            }
        }
        getOrderedData()

        function getOrderedColumns() {
            return Object.values(orderedData)
        }

        function reorderValues(row) {
            var orderedValues = []
            $.each(Object.keys(orderedData), function(index, value) {
                orderedValues.push(row[value])
            })
            return orderedValues
        }

        function formatValues(values) {
            var i;
            for (i = 0; i < values.length; i++) { 
                if (values[i] == null) {
                    values[i] = "N/A"
                }
            }
            return values
        }

        function detailFormatter(index, row) {
            var orderedColumns = getOrderedColumns()
            var orderedValues = reorderValues(row)
            orderedValues = formatValues(orderedValues)

            var html = ['<div class="detailview">']
            var i = 0
            var value
            $.each(orderedColumns, function (index, columnName) {
                // if (columnName == "Loan Amount") {
                //     value = amountFormatter(orderedValues[i]);
                if (columnName == "Industry (NAICS Code)") {
                    value = colOptions["naicscode"][orderedValues[i]]
                } else {
                    value = orderedValues[i]
                }
                html.push('<p><b>' + columnName + ':</b> ' + value + '</p>')
                i += 1
            })
            html.push('</div>')
            return html.join('')
        }
    
    // <!-- Reset table button -->
    
        $(function() {
            $resetButton.click(function () {
                requestCount = 0
                initial_state = true
                $('table').bootstrapTable('clearFilterControl')
                console.log("YOU JUST HIT RESET, IS THE COUNT ZERO and INITIAL STATE TRUE?")
                console.log(requestCount)
                console.log(initial_state)
                // $table.bootstrapTable('destroy')
                $table.bootstrapTable('refresh')
            })
        })
    
    // <!-- Loading screen overlay -->
        
            var type = 'bsGrow'
        
            function loadingTemplate(message) {
                
                if (type === 'fa') {
                    return '<i class="spinner-text" color:#007aff;font-size:32px;">Doing government work...&nbsp;&nbsp;</i><i style="color:#007aff;" class="fa fa-spinner fa-spin fa-fw fa-2x spinner-spinner"></i>'
                }
                if (type === 'pl') {
                    return '<div class="ph-item"><div class="ph-picture"></div></div>'
                }
                if (type === 'bsGrow') {
                    return '<i class="spinner-text text-primary";">Doing government work...&nbsp;&nbsp;</i><i class="spinner-grow text-primary spinner-spinner" role="status"><span class="sr-only">Loading...</span></i>'
                }
            }
        

    // <!-- Fix for Toggle All issue where table overlaps bottom pagination controls -->
    
        $('#table').on('post-body.bs.table', function (e, arg1, arg2) {
            console.log('POST BODY RAN, WHATS THE INITIAL STATE?')
            console.log(initial_state)
            $table.bootstrapTable('resetView')
            if (initial_state) {
                $('select[class*="bootstrap-table-filter-control-' + initialFilterColumn + '"]').val(initialFilterValue);
            }
            // $('div.hidden').fadeIn(2000).removeClass('hidden');
        });

        // $('#table').on('toggle.bs.table', function (e, arg1, arg2) {
        //     console.log('TOGGLE RAN')
        //         $table.bootstrapTable('resetView')
        //         console.log("THIS THING HAPPENED")
        //     });
        // 

// <!-- 
// $('#table').on('all.bs.table', function (data, event) {
//     console.log(event)
//     // console.log(data)
//     // $table.bootstrapTable('resetView')

//     });
//  -->

        var preBodyRanCount = 0
        $('#table').on('pre-body.bs.table', function (e, arg1, arg2) {
            console.log('PRE BODY RAN')
            // $('div.hidden').fadeIn(7000).removeClass('hidden');
            if (preBodyRanCount > 0) {
                $('div.hidden').fadeIn(500).removeClass('hidden');
            // setTimeout(() => { $('div.hidden').fadeIn(1000).removeClass('hidden'); }, 1);
            }
            console.log(preBodyRanCount)
            preBodyRanCount++;
        });


// Sidebar menu closing fix

var checkbox = document.querySelector("input[id=openSidebarMenu]");
var div = document.createElement('div');
div.id = 'left-nav-cover';

function sidebarMenuClick(element, eventName) {
    if (typeof checkbox != null) {
        document.addEventListener('click', function (e) {
            e = e || window.event;
            var target = e.target || e.srcElement;
            if ((target.getAttribute("id") != "sidebarMenu" && target.getAttribute("id") != "openSidebarMenu") && document.getElementById("openSidebarMenu").checked == true) {
                document.getElementById("openSidebarMenu").checked = false;
                sidebarMenuClick(checkbox, 'change');
                console.log("CHANGE")
            };
            if (target.getAttribute("id") == "openSidebarMenu" && document.getElementById("openSidebarMenu").checked == false) {
                document.getElementById("openSidebarMenu").checked = false;
                sidebarMenuClick(checkbox, 'change');
                console.log("CHANGE")
            };
        }, false);

        // function sidebarMenuClick(element, eventName) {
        //     var manualEvent = document.createEvent("HTMLEvents");
        //     manualEvent.initEvent(eventName, false, true);
        //     element.dispatchEvent(manualEvent);
        // }

        // var div = document.createElement('div');
        // div.id = 'left-nav-cover';
        document.getElementsByTagName('body')[0].appendChild(div);
        // checkbox.addEventListener('change', function () {
            if (checkbox.checked) {
                div.innerHTML = "<div id='left-nav-cover-inner'></div>";
                console.log("CREATED")
            } else {
                div.removeChild(document.getElementById("left-nav-cover-inner"));
                console.log("REMOVED")
            }
        // });
    }
}
// End sidebar menu closing fix

    // Cookie notification
        if (localStorage.getItem('cookieSeen') != 'shown') {
            $('.cookie-box').delay(5000).fadeIn();
        };

        $('.cookie-close').click(function () {
            $('.cookie-box').fadeOut();
            localStorage.setItem('cookieSeen', 'shown')
        })
    // End cookie notification