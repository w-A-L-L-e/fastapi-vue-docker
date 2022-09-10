<template>
  <div class="locale-selector">
    <select v-model="$i18n.locale" class="form-select">
      <option v-for="(locale, i) in locales" :key="`locale-${i}`" :value="locale">
        {{ locale }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "LocaleSwitcher",
  data() {
    return { locales: ["nl", "en"] };
  }
};
</script>

<style>
.locale-selector{
  margin-left: 10px;
}
</style>
