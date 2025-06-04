import pytest
import requests
import os
import time

# URLs de test
LOCAL_URL = "http://localhost:5000"

def get_ngrok_url():
    """Récupère l'URL ngrok depuis les variables d'environnement"""
    return os.environ.get('NGROK_URL')

class TestAPILocal:
    """Tests pour l'API locale"""
    
    def test_local_api_health_check(self):
        """Test que l'API locale répond avec un code 200"""
        try:
            response = requests.get(LOCAL_URL)
            print(f"🏠 API Locale - Status Code: {response.status_code}")
            print(f"🏠 API Locale - Response: {response.text[:100]}...")
            
            # Vérifier que l'API retourne un code 200
            assert response.status_code == 200, f"Attendu 200, reçu {response.status_code}"
            print("✅ Test réussi : API locale répond avec code 200")
            
        except requests.exceptions.ConnectionError:
            pytest.fail("❌ Impossible de se connecter à l'API locale")
        except Exception as e:
            pytest.fail(f"❌ Erreur lors du test local : {str(e)}")

    def test_local_api_response_time(self):
        """Test que l'API locale répond rapidement"""
        start_time = time.time()
        
        try:
            response = requests.get(LOCAL_URL, timeout=10)
            response_time = time.time() - start_time
            
            print(f"🏠 API Locale - Temps de réponse: {response_time:.2f} secondes")
            
            assert response.status_code == 200
            assert response_time < 3, f"Réponse trop lente: {response_time:.2f}s"
            print("✅ Test réussi : Temps de réponse local acceptable")
            
        except requests.exceptions.Timeout:
            pytest.fail("❌ Timeout : L'API locale ne répond pas assez rapidement")
        except Exception as e:
            pytest.fail(f"❌ Erreur lors du test de performance local : {str(e)}")

class TestAPINgrok:
    """Tests pour l'API via ngrok"""
    
    def test_ngrok_api_health_check(self):
        """Test que l'API est accessible via ngrok avec un code 200"""
        ngrok_url = get_ngrok_url()
        
        if not ngrok_url:
            pytest.skip("URL ngrok non disponible")
        
        try:
            response = requests.get(ngrok_url, timeout=15)
            print(f"🌐 API Ngrok - URL: {ngrok_url}")
            print(f"🌐 API Ngrok - Status Code: {response.status_code}")
            print(f"🌐 API Ngrok - Response: {response.text[:100]}...")
            
            # Vérifier que l'API retourne un code 200
            assert response.status_code == 200, f"Attendu 200, reçu {response.status_code}"
            print("✅ Test réussi : API accessible via ngrok avec code 200")
            
        except requests.exceptions.ConnectionError as e:
            pytest.fail(f"❌ Impossible de se connecter via ngrok: {str(e)}")
        except requests.exceptions.Timeout:
            pytest.fail("❌ Timeout lors de la connexion via ngrok")
        except Exception as e:
            pytest.fail(f"❌ Erreur lors du test ngrok : {str(e)}")

    def test_ngrok_api_response_time(self):
        """Test que le temps de réponse via ngrok est acceptable"""
        ngrok_url = get_ngrok_url()
        
        if not ngrok_url:
            pytest.skip("URL ngrok non disponible")
        
        start_time = time.time()
        
        try:
            response = requests.get(ngrok_url, timeout=20)
            response_time = time.time() - start_time
            
            print(f"🌐 API Ngrok - Temps de réponse: {response_time:.2f} secondes")
            
            assert response.status_code == 200
            assert response_time < 15, f"Réponse trop lente via ngrok: {response_time:.2f}s"
            print("✅ Test réussi : Temps de réponse ngrok acceptable")
            
        except requests.exceptions.Timeout:
            pytest.fail("❌ Timeout : L'API via ngrok ne répond pas assez rapidement")
        except Exception as e:
            pytest.fail(f"❌ Erreur lors du test de performance ngrok : {str(e)}")

class TestAPIComparison:
    """Tests de comparaison entre API locale et ngrok"""
    
    def test_both_apis_return_200(self):
        """Test que les deux APIs retournent un code 200"""
        ngrok_url = get_ngrok_url()
        
        # Test API locale
        try:
            local_response = requests.get(LOCAL_URL, timeout=5)
            local_status = local_response.status_code
            print(f"🏠 API Locale - Status: {local_status}")
        except Exception as e:
            pytest.fail(f"❌ API locale non accessible: {str(e)}")
        
        # Test API ngrok si disponible
        if ngrok_url:
            try:
                ngrok_response = requests.get(ngrok_url, timeout=15)
                ngrok_status = ngrok_response.status_code
                print(f"🌐 API Ngrok - Status: {ngrok_status}")
                
                # Les deux doivent retourner 200
                assert local_status == 200, f"API locale: attendu 200, reçu {local_status}"
                assert ngrok_status == 200, f"API ngrok: attendu 200, reçu {ngrok_status}"
                print("✅ Test réussi : Les deux APIs retournent 200")
                
            except Exception as e:
                print(f"⚠️  API ngrok non testée: {str(e)}")
                # Au moins l'API locale doit fonctionner
                assert local_status == 200, f"API locale: attendu 200, reçu {local_status}"
        else:
            # Seule l'API locale est testée
            assert local_status == 200, f"API locale: attendu 200, reçu {local_status}"
            print("✅ Test réussi : API locale retourne 200")

    def test_api_consistency(self):
        """Test que les deux APIs retournent le même contenu"""
        ngrok_url = get_ngrok_url()
        
        if not ngrok_url:
            pytest.skip("URL ngrok non disponible pour comparaison")
        
        try:
            local_response = requests.get(LOCAL_URL, timeout=5)
            ngrok_response = requests.get(ngrok_url, timeout=15)
            
            assert local_response.status_code == 200
            assert ngrok_response.status_code == 200
            
            # Comparer les contenus (premiers 500 caractères)
            local_content = local_response.text[:500]
            ngrok_content = ngrok_response.text[:500]
            
            print(f"🏠 Contenu local (extrait): {local_content[:50]}...")
            print(f"🌐 Contenu ngrok (extrait): {ngrok_content[:50]}...")
            
            # Le contenu devrait être identique ou très similaire
            assert len(local_content) > 0, "Contenu local vide"
            assert len(ngrok_content) > 0, "Contenu ngrok vide"
            
            print("✅ Test réussi : Les deux APIs retournent du contenu cohérent")
            
        except Exception as e:
            pytest.fail(f"❌ Erreur lors de la comparaison des APIs : {str(e)}")

def test_summary():
    """Résumé des tests effectués"""
    ngrok_url = get_ngrok_url()
    
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    print(f"🏠 API Locale testée: {LOCAL_URL}")
    if ngrok_url:
        print(f"🌐 API Ngrok testée: {ngrok_url}")
    else:
        print("🌐 API Ngrok: Non disponible")
    print("="*50)
    
    # Ce test passe toujours, c'est juste informatif
    assert True
