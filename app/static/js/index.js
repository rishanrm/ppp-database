

    // <!-- Get column options -->
    var colOptions;
    
    function getColumnNames() {
        console.log("IN GET COLUMNS")
        // console.log(params)
        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5000/header_options/', false);  // `false` makes the request synchronous
        request.send(null);

        if (request.status === 200) {
            colOptions = JSON.parse(request.responseText);
        }
        console.log("Got column names.")
    }
    getColumnNames()


    // <!-- Reset button -->
    
        var $table = $('#table')
        var $resetButton = $('#resetButton')
    

    // <!-- Get data -->
    
            function ajaxRequest(params) {
                var url = '/params'
                $.get(url + '?' + $.param(params.data))
                .then(function (res) {
                    params.success(res)
                    console.log(res)
                });
            };
    

    // <!-- Format loan amount data -->        
    
        function amountFormatter(value) {
            // return value.substring(0, value.length - 3)
            return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
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
                    return 'There are no loans in the center of that particular Venn diagram...<br><br>¯\\_(ツ)_/¯<br><br>but don\'t give up! Try it again with fewer filters.';
                },
                formatExport: function () {
                    return 'Export page'
                }
            };
            $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['en-US-custom']);
        })(jQuery);
    

    // <!-- Format data when a row is expanded -->
    

        var orderedData = {
            "loanamount": "Loan Amount ($)",
            "city": "City",
            "state": "State",                
            "zip": "ZIP Code",
            "naicscode": "NAICS Code",
            "businesstype": "Business Type",
            "raceethnicity": "Race/Ethnicity",
            "gender": "Gender",
            "veteran": "Veteran",
            "nonprofit": "Nonprofit",
            "jobsretained": "Jobs Retained",
            "dateapproved": "Date Approved",
            "lender": "Lender",
            "cd": "House District"
            }

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
                if (columnName == "Loan Amount ($)") {
                    value = amountFormatter(orderedValues[i]);
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
                $table.bootstrapTable('destroy')
                $table.bootstrapTable()
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
            console.log('POST BODY RAN')
            $table.bootstrapTable('resetView')
            $('div.hidden').fadeIn(2000).removeClass('hidden');
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


        $('#table').on('pre-body.bs.table', function (e, arg1, arg2) {
            console.log('PRE BODY RAN')
            $('div.hidden').fadeIn(2000).removeClass('hidden');

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



    // <!-- NOT CURRENTLY IN USE: -->

        // <!-- Fade in -->
        <!-- 
                $(document).ready(function () {
                    $('div.hidden').fadeIn(2000).removeClass('hidden');
                });
         -->

        // <!-- Action before table loads -->
        <!-- 
        $('#table').on('pre-body.bs.table', function (e, arg1, arg2) {
                    console.log('HELLO END')
                    var userJobTitles9
                    fetch("http://localhost:5000/data_test/businesstype.json")
                    .then(response => response.json())
                    .then(response => {
                        console.log("JSON IS THIS:")
                        console.log(response);
                        userJobTitles9 = response
                        console.log("ASSIGNED VARIABLE IS THIS:")
                        console.log(userJobTitles9);
                    }, error => {
                        console.error(error);
                    })
                });   
         -->

        // <!-- Action on change to columns -->
        <!-- 
            $('#table').on('column-switch.bs.table', function (e, arg1, arg2) {
                console.log('COLUMN SWITCH')
                $table.bootstrapTable('resetView')
                $table.bootstrapTable()
            })
            // onColumnSwitch
        
        -->

        // <!-- Data export -->
        <!-- 
            $(function() {
                $('#toolbar').find('select').change(function () {
                $table.bootstrapTable('destroy').bootstrapTable({
                    exportDataType: $(this).val(),
                    exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'pdf']
                })
                }).trigger('change')
            });
         -->

        // <!-- Column headers without search or filtering -->
        <!-- 
            $( "div:contains('Loan Amount'):last" ).parent().css({"vertical-align":"top"});
            $( "div:contains('Jobs Retained'):last" ).parent().css({"vertical-align":"top"});

            function headerStyle(column) {
                return {
                    loanamount: {
                    css: {'vertical-align': 'top'}
                    },
                    jobsretained: {
                    css: {'vertical-align': 'top'}
                    }
                }[column.field]
            }
         -->

        <!-- Export Data settings
        
            $table.bootstrapTable(
                {
                    exportTypes: ['csv', 'txt', 'doc', 'pdf', 'json', 'xml', 'sql'],
                    exportOptions: {
                        fileName: 'ppp_data',
                        ignoreColumn: [0]
                    }
                }
            )
         -->






    //     <!-- Old get data -->
    //     
    //         // let url = 'http://localhost:5000/data_test/businesstype.json';
    //         // userJobTitles2 = {
    //         //     'state': {
    //         //         Admin: 'Admin',
    //         //         IT: randomnum,
    //         //         General : 'General',
    //         //         Security : 'Security',
    //         //         CEO : 'CEO',
    //         //     },
    //         //     'zip': {
    //         //         Admin: 'Admin',
    //         //         CEO: randomnum
    //         //     },
    //         //     'businesstype': {
    //         //         BusinessType_1: 'BT 1',
    //         //         BusinessType_2: 'BT 2'
    //         //     }
    //         // };
    //         // console.log("FIRST PRINT")
    //         // console.log(userJobTitles2)

    //         // userJobTitles2 = fetch(url)
    //         // .then(res => res.json())
    //         // .then((out) => {
    //         // console.log('Checkout this JSON! ', out);
    //         // // userJobTitles2 = out
    //         // // console.log("IN METHOD:")
    //         // // console.log(userJobTitles2)
    //         // // console.log(userJobTitles2.businesstype)
    //         // })
    //         // .catch(err => { throw err });
    //         // console.log("SECOND PRINT")
    //         // console.log(userJobTitles2)
    //         // console.log("THIS IS THE VARIABLE LOGGED:")
    //         // console.log(userJobTitles2)
    //         // userJobTitles2 = $.get('http://localhost:5000/data_test/businesstype.json')
    //         // console.log("COLUMN JSON:")
    //         // console.log(userJobTitles2)
    //         // userJobTitles3 = {
    //         //     'state': {
    //         //         Admin: 'Admin',
    //         //         IT: randomnum,
    //         //         General : 'General',
    //         //         Security : 'Security',
    //         //         CEO : 'CEO',
    //         //     },
    //         //     'zip': {
    //         //         Admin: 'Admin',
    //         //         CEO: randomnum
    //         //     },
    //         //     'businesstype': {
    //         //         BusinessType_1: 'BT 1',
    //         //         BusinessType_2: 'BT 2'
    //         //     }
    //         // };
    //         // var userJobTitles = {
    //         //     'state': {
    //         //         Admin: 'Admin',
    //         //         IT: randomnum,
    //         //         General : 'General',
    //         //         Security : 'Security',
    //         //         CEO : 'CEO',
    //         //     },
    //         //     'zip': {
    //         //         Admin: 'Admin',
    //         //         CEO: randomnum
    //         //     }
    //         // };
    //         

    // 
    // //     var userJobTitles8
    // //     $.get("http://localhost:5000/data_test/businesstype.json", function(data){
    // //         userJobTitles8 = data
    // //         console.log(userJobTitles8)
    
    // //     })
    // //     userJobTitles8 = {
    // //         'state': {
    // //             Admin: 'Admin',
    // //             IT: randomnum,
    // //             General : 'General',
    // //             Security : 'Security',
    // //             CEO : 'CEO',
    // //         },
    // //         'zip': {
    // //             Admin: 'Admin',
    // //             CEO: randomnum
    // //         },
    // //         'businesstype': {
    // //             BusinessType_1: 'BT 1',
    // //             BusinessType_2: 'BT 2'
    // //         }
    // //     };
    // // 
    // 
    // //     console.log("OUTSIDE")
    // //     console.log(userJobTitles8)   
    // //     // var userJobTitles7 = new Object()

    //     // $.getJSON("http://localhost:5000/data_test/businesstype.json").then(
    //     //     function(data, userJobTitles7) {
    //     //         console.log('MY JSON:')
    //     //         console.log(Object.keys(data))
    //     //         userJobTitles7 = data

    //     //     }
    //     // )
    //     // console.log("OUTSIDE IT")
    //     // console.log(userJobTitles7)
    //     // var myjson = userJobTitles6

    //     // GET example
    //     // makeRequest('GET', "http://localhost:5000/data_test/businesstype.json").then(function(data){
    //     //     var userJobTitles4=JSON.parse(data);
    //     // console.log("NEW")
    //     // console.log(userJobTitles4)
    //     // console.log("NEWEST:")
    //     // console.log(userJobTitles6)
    //     // });
    // 

    // <!-- 
    // 
    // // var checkbox2 = document.querySelector(".toggle-all");
    // var checkbox2 = document.getElementsByClassName("toggle-all")[0];
    // console.log("AFTER VARIABLE DECLARATION")
    // console.log(checkbox2)
    // checkbox2.addEventListener( 'change', function() {
    //     if(this.checked) {
    //         console.log("QUERY CHECKED")
    //         // Checkbox is checked..
    //     } else {
    //         // Checkbox is not checked..
    //         console.log("QUERY UNCHECKED")
    //         // checkbox2.checked = true;
    //     }
    // });
    //  -->

    // <!-- Old table reset -->
    // <!-- 
    //     $(function() {
    //         $resetButton.click(function () {
    //             $table.bootstrapTable('removeAll')
    //             $table.bootstrapTable('resetSearch') // Clear value in global search box
    //             $table.bootstrapTable('clearFilterControl') //Unfilter results
    //             $table.bootstrapTable('refreshOptions', { //Clear column filters
    //             })
    //         })
    //     })
    //  -->

    // <!-- 
    // // function rebuild() {
    //     //     console.log("IN REBUILD")
    //     //     $('#table')
    //     //         .bootstrapTable('destroy')
    //     //         // .bootstrapTable()
    //     //         .bootstrapTable('showLoading')
    //     // }
        
    //     // rebuild()
    //  -->