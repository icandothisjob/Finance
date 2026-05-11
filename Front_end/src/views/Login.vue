<template>
  <div class="page" :style="{ backgroundImage: `url(${bgImg})` }">
    <!-- 整页暗色蒙版，让表单更清晰 -->
    <div class="page-mask"></div>

    <!-- 左侧：标题 + 表单 -->
    <div class="left">
      <div class="left-inner">
        <img :src="titleImg" alt="title" class="title-img" />

        <form class="form" @submit.prevent="onSubmit" autocomplete="off">
          <span class="form-title">Login</span>

          <!-- 一次性放置 SVG 渐变定义 -->
          <svg width="0" height="0" style="position:absolute">
            <defs>
              <linearGradient id="gradient-stroke" x1="0" y1="0" x2="1024" y2="1024" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="rgba(255,255,255,0.55)" />
                <stop offset="100%" stop-color="rgba(255,255,255,0.95)" />
              </linearGradient>
            </defs>
          </svg>

          <!-- 用户名 -->
          <div class="input-container">
            <svg class="field-icon" width="22" height="22" viewBox="0 0 1024 1024">
              <path d="M861.090909 786.385455a158.487273 158.487273 0 0 1-33.978182 101.934545A102.4 102.4 0 0 1 744.727273 930.909091H279.272727a102.167273 102.167273 0 0 1-82.152727-42.589091A158.952727 158.952727 0 0 1 162.909091 786.385455 744.727273 744.727273 0 0 1 167.563636 698.181818a467.083636 467.083636 0 0 1 17.221819-83.083636 279.272727 279.272727 0 0 1 31.883636-70.516364 150.807273 150.807273 0 0 1 51.2-48.64 144.523636 144.523636 0 0 1 73.541818-18.850909 235.752727 235.752727 0 0 0 170.589091 69.818182 235.752727 235.752727 0 0 0 170.821818-69.818182 142.429091 142.429091 0 0 1 73.541818 18.850909 153.134545 153.134545 0 0 1 51.2 48.64 279.272727 279.272727 0 0 1 31.883637 71.214546 462.894545 462.894545 0 0 1 17.221818 82.385454 800.116364 800.116364 0 0 1 4.421818 88.203637zM660.014545 154.530909A201.774545 201.774545 0 0 1 721.454545 302.545455a201.774545 201.774545 0 0 1-61.44 148.014545A201.774545 201.774545 0 0 1 512 512a201.774545 201.774545 0 0 1-148.014545-61.44A201.774545 201.774545 0 0 1 302.545455 302.545455a201.774545 201.774545 0 0 1 61.44-148.014546A201.774545 201.774545 0 0 1 512 93.090909a201.774545 201.774545 0 0 1 148.014545 61.44z"/>
            </svg>
            <input
              class="input"
              type="text"
              placeholder="Username"
              v-model="form.username"
              autocomplete="username"
            />
          </div>

          <!-- 密码 -->
          <div class="input-container">
            <svg class="field-icon" width="22" height="22" viewBox="0 0 1024 1024">
              <path d="M768.9216 422.72768 372.06016 422.72768C378.88 365.21984 329.37984 131.42016 512.2048 125.72672c173.83424-6.59456 146.78016 213.34016 146.78016 213.34016l85.13536 0.57344c0 0 24.73984-294.4-231.91552-295.8336C232.09984 58.01984 297.82016 377.18016 289.28 422.72768c1.98656 0 4.56704 0 7.29088 0-55.88992 0-101.21216 45.34272-101.21216 101.21216l0 337.38752c0 55.88992 45.34272 101.21216 101.21216 101.21216l472.35072 0c55.88992 0 101.21216-45.34272 101.21216-101.21216L870.13376 523.93984C870.13376 468.0704 824.79104 422.72768 768.9216 422.72768zM566.4768 717.02528l0 76.84096c0 18.57536-15.1552 33.73056-33.73056 33.73056-18.57536 0-33.73056-15.1552-33.73056-33.73056l0-76.84096c-20.09088-11.69408-33.73056-33.21856-33.73056-58.12224 0-37.2736 30.208-67.4816 67.4816-67.4816 37.2736 0 67.4816 30.208 67.4816 67.4816C600.22784 683.80672 586.58816 705.3312 566.4768 717.02528z"/>
            </svg>
            <input
              class="input"
              type="password"
              placeholder="Password"
              v-model="form.password"
              autocomplete="current-password"
              @keyup.enter="onSubmit"
            />
          </div>

          <!-- 验证码 -->
          <div class="input-container captcha-container">
            <svg class="field-icon" width="22" height="22" viewBox="0 0 1024 1024">
              <path d="M517.094527 1024c-153.345274 0-438.129353-228.234826-438.129353-444.242786V167.60995c0-10.189055 8.151244-17.830846 18.849751-18.340298l24.963184-0.509453c1.018905 0 98.324378-2.037811 198.686568-41.775124C423.864677 66.228856 490.093532 19.359204 491.112438 18.849751l14.774129-10.189054c3.056716-2.037811 7.132338-3.566169 11.20796-3.56617 4.075622 0 8.151244 1.018905 11.207961 3.56617l14.774129 10.698507c0.509453 0.509453 67.247761 47.379104 170.157214 88.135323 100.362189 39.737313 197.667662 41.775124 198.686567 41.775125l24.453731 0.509452c10.189055 0 18.849751 8.151244 18.849752 18.340299v412.147264c0 215.498507-284.78408 443.733333-438.129354 443.733333z m370.881592-808.501493c-37.699502-3.056716-117.174129-12.736318-199.196019-45.341293-84.569154-33.114428-146.212935-70.304478-171.685573-87.116418-25.472637 16.302488-87.116418 54.00199-171.685572 87.116418-82.021891 32.604975-160.987065 42.284577-199.19602 45.341293v364.258707c0 169.138308 248.103483 376.485572 370.881592 376.485572 47.379104 0 140.099502-38.718408 230.78209-123.287562 87.625871-81.512438 140.099502-176.270647 140.099502-253.19801V215.498507z m-406.03383 433.544279c-6.113433 6.622886-14.774129 10.189055-23.944279 10.189055-9.170149 0-17.321393-3.566169-23.944279-10.189055l-101.381094-101.890547a33.827662 33.827662 0 0 1 0-47.888557c13.245771-13.245771 34.133333-13.245771 47.379104-0.509453l0.509453 0.509453 77.436816 77.946268 195.120398-196.648756c12.736318-13.245771 34.133333-13.245771 47.379104-0.509453l0.509453 0.509453c13.245771 13.245771 13.245771 34.642786 0 47.888557l-219.064676 220.593035z"/>
          </svg>
            <input
              class="input"
              type="text"
              placeholder="Captcha"
              maxlength="4"
              v-model="form.captcha"
              @keyup.enter="onSubmit"
            />
            <canvas
              ref="captchaCanvas"
              class="captcha-canvas"
              width="92"
              height="32"
              title="点击刷新"
              @click="refreshCaptcha"
            ></canvas>
          </div>

          <!-- 登录按钮 -->
          <div class="login-button">
            <input
              class="input"
              type="submit"
              :value="loading ? 'Signing in...' : 'Login'"
              :disabled="loading"
            />
          </div>

          <div class="texture"></div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast } from '../utils/toast'
import { login as apiLogin } from '../api/auth'
import { setToken, setUser } from '../utils/auth'
import titleImg from '../img/Title.png'
import bgImg from '../img/bg.png'

const router = useRouter()
const route = useRoute()
const captchaCanvas = ref(null)
const loading = ref(false)
const captchaCode = ref('')

const form = reactive({
  username: 'admin',
  password: 'admin',
  captcha: '',
})

function genCode(len = 4) {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let s = ''
  for (let i = 0; i < len; i++) {
    s += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return s
}

function drawCaptcha() {
  const canvas = captchaCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width
  const h = canvas.height
  ctx.clearRect(0, 0, w, h)

  ctx.fillStyle = 'rgba(255, 224, 166, 0.06)'
  ctx.fillRect(0, 0, w, h)

  const code = genCode(4)
  captchaCode.value = code

  const colors = ['#ffe0a6', '#ffffff', '#d6b87e', '#ffeec0', '#bca06a']
  const charSlot = w / code.length
  for (let i = 0; i < code.length; i++) {
    ctx.save()
    ctx.font = 'bold 22px sans-serif'
    ctx.fillStyle = colors[Math.floor(Math.random() * colors.length)]
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    const x = charSlot * i + charSlot / 2 + (Math.random() * 4 - 2)
    const y = h / 2 + (Math.random() * 4 - 2)
    ctx.translate(x, y)
    ctx.rotate(((Math.random() - 0.5) * Math.PI) / 8)
    ctx.fillText(code.charAt(i), 0, 0)
    ctx.restore()
  }
  for (let i = 0; i < 3; i++) {
    ctx.strokeStyle =
      colors[Math.floor(Math.random() * colors.length)] + '88'
    ctx.beginPath()
    ctx.moveTo(Math.random() * w, Math.random() * h)
    ctx.lineTo(Math.random() * w, Math.random() * h)
    ctx.stroke()
  }
  for (let i = 0; i < 25; i++) {
    ctx.fillStyle =
      colors[Math.floor(Math.random() * colors.length)] + '66'
    ctx.fillRect(Math.random() * w, Math.random() * h, 1.5, 1.5)
  }
}

function refreshCaptcha() {
  drawCaptcha()
  form.captcha = ''
}

async function onSubmit() {
  if (!form.username || !form.password) {
    toast.warning('请输入用户名和密码')
    return
  }
  if (!form.captcha) {
    toast.warning('请输入验证码')
    return
  }
  if (form.captcha.toLowerCase() !== captchaCode.value.toLowerCase()) {
    toast.error('验证码错误')
    refreshCaptcha()
    return
  }

  loading.value = true
  try {
    const res = await apiLogin({
      username: form.username,
      password: form.password,
    })
    setToken(res.access_token)
    setUser(res.user)
    toast.success(`欢迎回来，${res.user.nickname || res.user.username}`)
    const redirect = route.query.redirect
      ? decodeURIComponent(route.query.redirect)
      : '/dashboard'
    router.replace(redirect)
  } catch {
    refreshCaptcha()
  } finally {
    loading.value = false
  }
}

onMounted(drawCaptcha)
</script>

<style scoped>
/* ===================== 整页：背景图铺满 ===================== */
.page {
  width: 100vw;
  height: 100vh;
  background-color: #000;
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  position: relative;
  overflow: hidden;
}
/* 暗色渐变蒙版：左侧深一点，让表单更清晰 */
.page-mask {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0.4) 35%,
    rgba(0, 0, 0, 0.15) 100%
  );
  pointer-events: none;
  z-index: 1;
}

/* ===================== 左侧：标题 + 表单 ===================== */
.left {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 32px 8vw;
}
.left-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 22px;
}
.title-img {
  max-width: 200px;
  max-height: 14vh;
  object-fit: contain;
  filter: drop-shadow(0 8px 24px rgba(255, 224, 166, 0.25));
  user-select: none;
  -webkit-user-drag: none;
}

/* 小屏：表单居中 */
@media (max-width: 900px) {
  .left {
    justify-content: center;
    padding: 24px 16px;
  }
  .title-img {
    max-width: 180px;
    max-height: 12vh;
  }
}

/* 手机端：表单宽度自适应、内边距压缩 */
@media (max-width: 600px) {
  .page { min-height: 100dvh; }
  .left {
    padding: 16px 12px;
    padding-top: max(16px, env(safe-area-inset-top));
    padding-bottom: max(16px, env(safe-area-inset-bottom));
  }
  .title-img { max-width: 150px; max-height: 10vh; }
}
@media (max-width: 480px) {
  .form {
    width: 100% !important;
    max-width: 360px;
    padding: 2.2rem 1.6rem !important;
    gap: 1.6rem !important;
  }
}

/* ===================== 表单（暗色霓虹风格，平时弱化、悬停高亮） ===================== */
.form {
  padding: 3.4rem 3rem;
  display: grid;
  place-items: center;
  gap: 2.6rem;
  border: 1px solid transparent;
  border-image: linear-gradient(
    transparent,
    rgba(255, 224, 166, 0.28),
    transparent
  ) 1;
  border-width: 0 1px 0 1px;
  background:
    radial-gradient(100% 61.73% at 100% 50%, rgba(255, 224, 166, 0.04) 0%, transparent 100%),
    radial-gradient(91.09% 56.23% at 0% 50%, rgba(255, 224, 166, 0.04) 0%, transparent 100%);
  position: relative;
  width: 420px;
  transition: border-image 0.3s ease, background 0.3s ease;
}
/* 触摸 / 聚焦表单：左右描边变亮，整体淡金辉光 */
.form:hover,
.form:focus-within {
  border-image: linear-gradient(
    transparent,
    rgba(255, 224, 166, 0.85),
    transparent
  ) 1;
  background:
    radial-gradient(100% 61.73% at 100% 50%, rgba(255, 224, 166, 0.1) 0%, transparent 100%),
    radial-gradient(91.09% 56.23% at 0% 50%, rgba(255, 224, 166, 0.1) 0%, transparent 100%);
}
.form::before,
.form::after {
  content: '';
  position: absolute;
  border: inherit;
  z-index: -1;
}
.form::before {
  inset: -1rem;
  opacity: 0.06;
}
.form::after {
  inset: -2rem;
  opacity: 0.02;
}

.form-title {
  font-size: 2.1rem;
  font-weight: 700;
  text-align: center;
  letter-spacing: 1rem;
  text-transform: uppercase;
  background: linear-gradient(rgb(170, 170, 170), rgb(78, 78, 78));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  padding-left: 1rem;
  transition: filter 0.3s ease;
}
/* 触摸 / 聚焦表单时：LOGIN 渐变变成淡金色，并加发光 */
.form:hover .form-title,
.form:focus-within .form-title {
  background: linear-gradient(#ffe0a6, #c9a86b);
  -webkit-background-clip: text;
  background-clip: text;
  filter: drop-shadow(0 0 8px rgba(255, 224, 166, 0.45));
}

.input-container {
  display: flex;
  align-items: center;
  width: 100%;
  background: radial-gradient(
    47.3% 73.08% at 50% 94.23%,
    rgba(255, 255, 255, 0.1) 5%,
    rgba(0, 0, 0, 0) 100%
  );
  border: 1px solid transparent;
  border-image: radial-gradient(
      circle,
      rgba(255, 255, 255, 0.445) 0%,
      rgba(0, 0, 0, 0) 100%
    ) 1;
  border-width: 0 0 1px 0;
  transition: all 0.2s ease-in-out;
}
.input-container svg {
  flex-shrink: 0;
  margin-left: 4px;
}
.input-container .field-icon {
  fill: rgba(255, 255, 255, 0.55);
  transition: fill 0.2s ease-in-out, filter 0.2s ease-in-out;
}
.input-container .input {
  flex: 1;
  background: none;
  border: none;
  padding: 0.75rem 1rem;
  color: white;
  font-size: 15px;
  letter-spacing: 1px;
  width: 100%;
}
.input-container .input::placeholder {
  color: rgba(255, 255, 255, 0.35);
}
.input-container .input:focus {
  outline: none;
  color: #ffe0a6;
}
.input-container:focus-within {
  background: radial-gradient(
    47.3% 73.08% at 50% 94.23%,
    rgba(255, 224, 166, 0.1) 5%,
    rgba(0, 0, 0, 0) 100%
  );
  border-image: radial-gradient(circle, #ffe0a6 0%, transparent 100%) 1;
}
.input-container:focus-within .field-icon {
  fill: #ffe0a6;
  filter: drop-shadow(0 0 4px rgba(255, 224, 166, 0.6));
}

.captcha-container .input {
  flex: 1;
  min-width: 0;
}
.captcha-canvas {
  flex-shrink: 0;
  width: 92px;
  height: 32px;
  margin-left: 6px;
  cursor: pointer;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 224, 166, 0.25);
  transition: border-color 0.2s ease;
}
.captcha-canvas:hover {
  border-color: rgba(255, 224, 166, 0.6);
}

.login-button {
  width: 100%;
  position: relative;
  transition: all 0.2s ease-in-out;
  display: flex;
  justify-content: center;
}
.login-button .input {
  cursor: pointer;
  padding: 1rem;
  width: 100%;
  background:
    radial-gradient(100% 45% at 100% 50%, rgba(255, 224, 166, 0.06) 0%, rgba(115, 115, 115, 0) 100%),
    radial-gradient(100% 45% at 0% 50%, rgba(255, 224, 166, 0.06) 0%, rgba(115, 115, 115, 0) 100%);
  border: 1px solid transparent;
  border-image: linear-gradient(
    transparent,
    rgba(255, 224, 166, 0.45),
    transparent
  ) 1;
  border-width: 0 1px 0 1px;
  text-align: center;
  color: #ffe0a6;
  font-size: 1.1rem;
  letter-spacing: 4px;
  text-transform: uppercase;
}
.login-button .input:disabled {
  cursor: not-allowed;
  color: rgba(255, 224, 166, 0.5);
}
.login-button::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: linear-gradient(0deg, rgba(255, 255, 255, 0.376) 0.5px, transparent 0.5px);
  background-size: 0.1px 3px;
  mix-blend-mode: soft-light;
  -webkit-mask-image:
    radial-gradient(40% 45% at 100% 50%, white 0%, transparent 100%),
    radial-gradient(40% 45% at 0% 50%, white 0%, transparent 100%);
  mask-image:
    radial-gradient(40% 45% at 100% 50%, white 0%, transparent 100%),
    radial-gradient(40% 45% at 0% 50%, white 0%, transparent 100%);
}
.login-button:hover:not(:has(.input:disabled)) {
  animation: flicker 0.5s infinite;
  width: 105%;
}
.login-button:active:not(:has(.input:disabled)) {
  width: 95%;
}

.texture {
  position: absolute;
  background-image: linear-gradient(0deg, rgba(255, 255, 255, 0.35) 1px, transparent 1px);
  background-size: 1px 6px;
  inset: 0;
  opacity: 0.4;
  mix-blend-mode: soft-light;
  -webkit-mask-image:
    radial-gradient(22% 40% at 100% 50%, white 0%, transparent 100%),
    radial-gradient(22% 40% at 0% 50%, white 0%, transparent 100%);
  mask-image:
    radial-gradient(22% 40% at 100% 50%, white 0%, transparent 100%),
    radial-gradient(22% 40% at 0% 50%, white 0%, transparent 100%);
  pointer-events: none;
  animation: movingLines 1.2s linear infinite;
  transition: opacity 0.3s ease, background-image 0.3s ease;
}
/* 触摸 / 聚焦表单：装饰线条变成淡金色 + 加亮 + 加快流动 */
.form:hover .texture,
.form:focus-within .texture {
  opacity: 1;
  background-image: linear-gradient(0deg, rgba(255, 224, 166, 0.7) 1px, transparent 1px);
  animation-duration: 0.6s;
}

@keyframes flicker {
  0%   { filter: brightness(100%); }
  10%  { filter: brightness(80%); }
  20%  { filter: brightness(120%); }
  30%  { filter: brightness(90%); }
  40%  { filter: brightness(110%); }
  50%  { filter: brightness(100%); }
  60%  { filter: brightness(85%); }
  70%  { filter: brightness(95%); }
  80%  { filter: brightness(105%); }
  90%  { filter: brightness(115%); }
  100% { filter: brightness(100%); }
}
@keyframes movingLines {
  0%   { background-position: 0 0; }
  100% { background-position: 0 5px; }
}
</style>
