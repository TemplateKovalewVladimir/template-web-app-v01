<script lang="tsx">
import { defineComponent } from 'vue'

export default defineComponent({
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Layout',
  setup() {
    return () => (
      <div>
        <router-view />
      </div>
    )
  }
})
</script>

<style lang="less" scoped></style>
