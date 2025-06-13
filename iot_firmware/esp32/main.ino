// Definições para o ESP32 e o Termistor NTC
// THERMISTOR_PIN: Define o pino GPIO 34 do ESP32 para a leitura analógica do sensor de temperatura.
//                 GPIO 34 é um dos pinos ADC (Conversor Analógico-Digital) do ESP32, adequado para sensores analógicos.
const int THERMISTOR_PIN = 34; 

// NOMINAL_RESISTANCE: Resistência do termistor em sua temperatura nominal (25°C), tipicamente 10kΩ.
const int NOMINAL_RESISTANCE = 10000; 

// NOMINAL_TEMPERATURE: Temperatura de referência para a resistência nominal, em graus Celsius.
const int NOMINAL_TEMPERATURE = 25; 

// B_COEFFICIENT: Coeficiente Beta (B) do termistor. Este valor, junto com a resistência nominal,
//                é usado na equação de Steinhart-Hart para converter resistência em temperatura.
//                Um valor típico para termistores NTC de 10kΩ é 3950.
const int B_COEFFICIENT = 3950; 

// SERIES_RESISTANCE: Resistência em série com o termistor no circuito divisor de tensão.
//                    Como estamos usando uma placa de sensor (KY-013) que já integra essa resistência,
//                    este valor reflete a resistência interna da placa para os cálculos.
const int SERIES_RESISTANCE = 10000; 

// Função setup(): Executada uma única vez quando o ESP32 é iniciado ou reiniciado.
void setup() {
  // Serial.begin(baudRate): Inicializa a comunicação serial entre o ESP32 e o Serial Monitor.
  //                        115200 bps (bits por segundo) é uma velocidade comum e rápida para debug.
  Serial.begin(115200); 

  // analogReadResolution(bits): Define a resolução do ADC. O ESP32 pode usar até 12 bits,
  //                             o que significa leituras de 0 a 4095 (2^12 - 1).
  //                             Uma resolução maior oferece maior precisão nas leituras analógicas.
  analogReadResolution(12); 
}

// Função loop(): Executada repetidamente após a função setup().
void loop() {
  // Leitura do valor analógico: Lê o valor bruto do ADC do pino especificado.
  // O valor retornado estará entre 0 e 4095, proporcional à tensão no pino.
  int adcValue = analogRead(THERMISTOR_PIN);

  // Cálculo da resistência do termistor:
  // Esta fórmula deriva da análise do divisor de tensão e é usada para obter
  // a resistência atual do termistor com base na leitura do ADC e na resistência em série.
  float resistance = SERIES_RESISTANCE / ((4095.0 / adcValue) - 1);

  // Cálculo da temperatura em Celsius usando a equação de Steinhart-Hart (simplificada):
  // Esta equação é um modelo matemático amplamente utilizado para converter a resistência
  // de um termistor NTC para temperatura.
  float steinhart;
  steinhart = resistance / NOMINAL_RESISTANCE;     // Passo 1: R/R0 (resistência atual sobre resistência nominal)
  steinhart = log(steinhart);                      // Passo 2: ln(R/R0) (logaritmo natural)
  steinhart /= B_COEFFICIENT;                      // Passo 3: Dividido pelo coeficiente Beta
  steinhart += 1.0 / (NOMINAL_TEMPERATURE + 273.15); // Passo 4: Adiciona 1/T0 (T0 em Kelvin)
  steinhart = 1.0 / steinhart;                     // Passo 5: Inverte para obter a temperatura em Kelvin
  float temperatureC = steinhart - 273.15;         // Passo 6: Converte de Kelvin para Celsius (subtrai 273.15)

  // Impressão dos valores no Monitor Serial:
  // Envia os valores lidos e calculados para o Serial Monitor do Wokwi.
  // O "\t" insere um caractere de tabulação para organizar a saída em colunas.
  Serial.print("Valor ADC: ");
  Serial.print(adcValue);
  Serial.print("\tResistencia Calculada: ");
  Serial.print(resistance);
  Serial.print(" ohms\tTemperatura Calculada: ");
  Serial.print(temperatureC);
  Serial.println(" °C"); // Serial.println adiciona uma quebra de linha

  // delay(milissegundos): Pausa a execução do loop por um tempo especificado.
  // Usamos 1000 ms (1 segundo) para simular uma amostragem de dados a cada segundo (1 Hz).
  delay(1000); 
}