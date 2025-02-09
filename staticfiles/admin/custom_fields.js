document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("custom-fields-container");
  if (!container) {
    console.error("カスタムフィールドコンテナが見つかりませんでした");
    return;
  }

  // Djangoから受け取った初期値を取得
  const initialData = JSON.parse(container.getAttribute("data-fields") || "[]");

  const app = Vue.createApp({
    data() {
      return {
        fields: initialData,      // 既存のフィールド一覧 [{key,value},...]
        newFieldKey: "",          // 新規追加用のフィールド名だけ
      };
    },
    methods: {
      addField() {
        const key = this.newFieldKey.trim();
        if (key !== "") {
          // 新しいフィールドを追加（valueは空文字で初期化）
          this.fields.push({ key: key, value: "" });
          this.newFieldKey = "";
        }
      },
      removeField(index) {
        this.fields.splice(index, 1);
      },
      updateHiddenField() {
        // Djangoのフォーム上の隠しフィールドにJSONを反映
        const hiddenField = document.getElementById("id_custom_fields");
        if (hiddenField) {
          hiddenField.value = JSON.stringify(this.fields);
        }
      },
    },
    watch: {
      // fieldsに変化があったら隠しフィールドを更新
      fields: {
        handler() {
          this.updateHiddenField();
        },
        deep: true,
      },
    },
    mounted() {
      // マウントされたタイミングでも反映
      this.updateHiddenField();
    },
  });

  app.mount(container);
});
