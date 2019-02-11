Rails.application.routes.draw do
  get 'welcome/index'
  resources :triples
  root 'triples#new'
  post 'triples/do_test'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
