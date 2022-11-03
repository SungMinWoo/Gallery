const search = document.getElementById('search_box');
const tableForm = document.getElementById('table-form');
const searchForm = document.getElementById('search-form');

tableForm.addEventListener('submit', e => {
    /**
        데이터가 선택되지 않았을때 submit 멈춤
    */
    var check_value = document.querySelectorAll("input[name='updateList']:checked").length;
    if (check_value === 0){
        alert('처리할 데이터를 선택해주시기 바랍니다.');
        e.preventDefault();
    }
});

searchForm.addEventListener('submit', e => {
    /**
        검색어가 없을때 submit 멈춤
    */
    if (search.value.length === 0){
        alert('검색어를 입력해주세요.');
        e.preventDefault();
    }
});

// table csv 다운
function download_table_as_csv(table_id, separator = ',') {
    var rows = document.querySelectorAll('#' + table_id + ' tr');
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            data = data.replace(/"/g, '""');
            // data 가장 윗줄부터 읽어 내려감
            row.push('"' + data + '"');
        }
        // row.join(separator)) // list형 row 데이터를 , 구분자로 합침
        csv.push(row.join(separator));
    }
    var csv_string = csv.join('\n');
    var filename = '작가 등록 조회_' + new Date().toLocaleDateString() + '.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,%EF%BB%BF' + encodeURIComponent(csv_string)); // 글자 깨짐 방지 깨짐
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}