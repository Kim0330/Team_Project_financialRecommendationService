<template>
  <div class="map-container">
    <div class="search-filters">
      <div class="location-filter">
        <h1>주변 은행 찾기</h1>
        <hr>
        <select v-model="selectedProvince" @change="handleProvinceChange">
          <option value="">시/도 선택</option>
          <option v-for="info in mapStore.infos" :key="info.id" :value="info.prov">
            {{ info.prov }}
          </option>
        </select>

        <select v-model="selectedCity" :disabled="!selectedProvince">
          <option value="">시/군/구 선택</option>
          <option v-for="city in availableCities" :key="city" :value="city">
            {{ city }}
          </option>
        </select>
      </div>

      <div class="bank-filter">
        <select v-model="selectedBank">
          <option value="">은행 선택</option>
          <option v-for="bank in mapStore.banks" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>

      <button @click="searchBanks" :disabled="!isSearchable || !isMapReady">
        검색
      </button>
    </div>

    <div id="map" ref="mapContainer"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useMapStore } from '../stores/map'

const mapStore = useMapStore()
const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const isMapReady = ref(false)

// 선택된 값들을 저장할 상태
const selectedProvince = ref('')
const selectedCity = ref('')
const selectedBank = ref('')

// 카카오맵 관련 서비스 객체들
let geocoder = null
let places = null

// 선택된 도시에 따른 사용 가능한 도시 목록
const availableCities = computed(() => {
  if (!selectedProvince.value) return []
  const provinceInfo = mapStore.infos.find(info => info.prov === selectedProvince.value)
  return provinceInfo ? provinceInfo.city : []
})

// 검색 버튼 활성화 여부
const isSearchable = computed(() => {
  return selectedProvince.value && selectedCity.value && selectedBank.value
})

// 도/시 선택 변경 시 하위 도시 초기화
const handleProvinceChange = () => {
  selectedCity.value = ''
}

// 마커 생성 함수
const createMarker = (position, title) => {
  const markerPosition = new kakao.maps.LatLng(position.lat, position.lng)
  
  const marker = new kakao.maps.Marker({
    position: markerPosition,
    map: map.value
  })

  const infowindow = new kakao.maps.InfoWindow({
    content: `<div style="padding:5px;font-size:12px;">${title}</div>`
  })

  kakao.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map.value, marker)
  })

  return { marker, infowindow }
}

// 기존 마커 제거
const clearMarkers = () => {
  markers.value.forEach(marker => {
    marker.marker.setMap(null)
    marker.infowindow.close()
  })
  markers.value = []
}

// 은행 검색 함수
const searchBanks = async () => {
  if (!isMapReady.value) return
  
  clearMarkers()
  
  const address = `${selectedProvince.value} ${selectedCity.value}`
  
  geocoder.addressSearch(address, (result, status) => {
    if (status === kakao.maps.services.Status.OK) {
      const coords = new kakao.maps.LatLng(result[0].y, result[0].x)
      map.value.setCenter(coords)
      
      places.keywordSearch(`${selectedCity.value} ${selectedBank.value}`, (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
          result.forEach(place => {
            const marker = createMarker({
              lat: place.y,
              lng: place.x
            }, place.place_name)
            markers.value.push(marker)
          })
        }
      }, {
        location: coords,
        radius: 5000
      })
    }
  })
}

// 카카오맵 초기화 함수
const initializeKakaoMap = () => {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&libraries=services&autoload=false`
  script.async = true
  
  script.onload = () => {
    window.kakao.maps.load(() => {
      const options = {
        center: new window.kakao.maps.LatLng(37.566826, 126.9786567),
        level: 5
      }
      
      map.value = new window.kakao.maps.Map(mapContainer.value, options)
      geocoder = new window.kakao.maps.services.Geocoder()
      places = new window.kakao.maps.services.Places()
      
      isMapReady.value = true
    })
  }
  
  document.head.appendChild(script)
}

// 컴포넌트 마운트/언마운트 처리
onMounted(() => {
  initializeKakaoMap()
})

onUnmounted(() => {
  clearMarkers()
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.search-filters {
  padding: 1rem;
  display: flex;
  gap: 1rem;
  background-color: #f5f5f5;
}

.location-filter,
.bank-filter {
  display: flex;
  gap: 0.5rem;
}

select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

#map {
  flex: 1;
  min-height: 500px;
}
</style>