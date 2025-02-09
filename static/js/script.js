document.addEventListener('DOMContentLoaded', function() {
    const addRowButton = document.getElementById('add-row');
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    if (addRowButton && totalForms) {
        addRowButton.addEventListener('click', function() {
            const grid = document.querySelector('.docspdf__grid');
            const templateRow = grid.querySelector('.area.value');

            if (!templateRow) {
                console.error("エラー: クローンする行が見つかりません");
                return;
            }

            const newIndex = parseInt(totalForms.value);
            const newRow = templateRow.cloneNode(true);

            // 更新されたインデックスを設定
            newRow.innerHTML = newRow.innerHTML.replace(/-\d+-/g, `-${newIndex}-`);
            grid.appendChild(newRow);

            // `TOTAL_FORMS` の値を更新
            totalForms.value = newIndex + 1;

            // 各フィールドの値をクリア
            const inputs = newRow.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.value = '';
                input.name = input.name.replace(/-\d+-/g, `-${newIndex}-`);
                input.id = input.id.replace(/-\d+-/g, `-${newIndex}-`);
            });
        });
    }

    // 削除ボタンの動作を追加（削除ボタンを JS で作らない代わりに、削除処理は実装）
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-row')) {
            const row = event.target.closest('.area.value');
            row.remove();

            // `TOTAL_FORMS` の値を減らす
            totalForms.value = Math.max(0, parseInt(totalForms.value) - 1);
        }
    });
});



jQuery(document).ready(function($) {
    // ドロワーの初期化
    $('.drawer').drawer();

    // ナビゲーション内のリンクがクリックされたときにドロワーを閉じる
    $('.drawer-menu a').on('click', function() {
        $('.drawer').drawer('close');
    });
});


jQuery(document).ready(function($) {
    $('[data-toggle]').on('click', function() {
        // クリックされたボタンのdata-toggle属性の値を取得
        var target = $(this).data('toggle');

        // 同じエリア内の対応するdata-content属性の要素をスライドで開閉
        var content = $('[data-content="' + target + '"]');
        content.slideToggle(300);

        // クリックした要素（ボタン）に active クラスをトグル
        $(this).toggleClass('active');
    });
});



