from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import escape
import json
from .models import InventoryItem

# custom_fields を隠しフィールドにするフォーム
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = '__all__'
        widgets = {
            'custom_fields': forms.HiddenInput(),
        }

class InventoryItemAdmin(admin.ModelAdmin):
    form = InventoryItemForm
    list_display = ('product_name', 'stock_count', 'product_code', 'updated_at')
    fields = (
        'product_name',
        'stock_count',
        'product_code',
        'notes',
        'image',
        'custom_fields',          # 実際は HiddenInput
        'custom_fields_display',  # Vue.js で見せる領域
    )
    readonly_fields = ('custom_fields_display',)

    class Media:
        js = (
            'https://unpkg.com/vue@3/dist/vue.global.prod.js',  # Vue.js
            'admin/custom_fields.js',  # カスタムフィールド用スクリプト
        )

    def custom_fields_display(self, obj):
        default_fields = [{"key": "新しいフィールド", "value": ""}]
        data_fields = json.dumps(obj.custom_fields if obj and obj.custom_fields else default_fields)

        # Vue.js 用のテンプレート。
        # 既存のfieldsを一覧表示し、追加用に「keyのみ」入力するフィールドを別で用意。
        return mark_safe(f"""
            <div id="custom-fields-container" data-fields='{escape(data_fields)}' data-v-app="">
                <!-- 既存のフィールドを表示する部分 -->
                <div v-for="(field, index) in fields" :key="index" style="margin-bottom: 5px;">
                  <div>
                    <strong>{{{{ field.key }}}}</strong>
                    <button type="button" @click="removeField(index)" style="margin-left: 10px;">削除</button>
                  </div>
                  <!-- 値を入力する欄 -->
                  <input
                    v-model="field.value"
                    placeholder="値を入力 (例: 50cm)"
                    style="width: 300px; margin-bottom: 10px;"
                  />
                  <hr>
                </div>

                <!-- 新規追加用 -->
                <div style="margin-top: 10px;">
                  <input
                    v-model="newFieldKey"
                    placeholder="新しいフィールド名 (例: 寸法)"
                    style="width: 300px;"
                  />
                  <button type="button" @click="addField">追加</button>
                </div>
            </div>
        """)

    custom_fields_display.short_description = "カスタムフィールド"

admin.site.register(InventoryItem, InventoryItemAdmin)
