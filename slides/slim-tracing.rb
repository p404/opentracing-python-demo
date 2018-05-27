# encoding: utf-8
center <<-EOS

  ┌────────────────────────────────────────┐
  │ Tracing Microservices with \e[1mOpenTracing\e[0m │
  └────────────────────────────────────────┘

  pablo[at]sequel[dot]ninja 
  © 2017
EOS

center <<-EOS
\e[1mPablo Opazo\e[0m

\e[1mSenior DevOps Engineer\e[0m

https://github.com/p404
pablo[at]sequel[dot]ninja 
EOS

block <<-EOS
  Agenda:

   1.- Intro___________________
   2.- Tracing?________________
   4.- Tracers_________________
   5.- Opentracing_____________
   6.- Tracing with opentracing
   7.- Demo____________________
   8.- Questions_______________
EOS

section "| Intro |" do
end

section "\e[1mTracing?\e[0m" do
  block <<-EOS
    Trace: A trace tells a story of a transaction workflow as it propagates.
  EOS

  block <<-EOS
    \e[1mweb application\e[0m
    ├─login
    │ ├─validates email
    │ └─send request to another service
    │   └─verify password
    │     └─\e[1mSQL Query\e[0m
    └ log out
  EOS
end

section "\e[1mMicroservices Tracers\e[0m" do
  block <<-EOS
    * Stackdriver (Google)
    * Zipkin (Twitter)
    * \e[1mJaeger\e[0m (Uber)
  EOS

  center <<-EOS
  \e[1mJaeger Architecture\e[0m
  
  ───────────────────────────────────────────
  
  +- Jager-client --> Jager-agent --> Jaeger-collector -+
                                                                  |                                 
                                                                   V                                  
    +- Jager-ui --> Jaeger-query --> Storage -+
                                  (Cassandra)
                                  or
                                  (Elasticsearch)
                                  
  EOS
end

section "\e[1mOpenTracing\e[0m" do
  center <<-EOS
    OpenTracing offers a consistent, vendor neutral, expressive API to do tracing.
  EOS

  block <<-EOS
  Features:
  * Has a lot helpers libraries in many languages.
  * Makes it easy for developers to add (or switch) tracing implementation with a configuration change.
  * You can change the Tracer implementation anytime (Zipkin, Jaeger, Lightstep, etc)
  * The OpenTracing project is sponsored and maintained by the Cloud Native Computing Foundation (CNCF)
  EOS
  
  block <<-EOS
  \e[1mOpenTracing Concepts\e[0m
  ────────────────────
     
          Span
     
     Inject/Extract
  EOS
end

section "Tracing with \e[1mOpenTracing\e[0m in python" do
  code <<-EOS
    Initializing a tracer implementation(Jaeger)
    ────────────────────────────────────────
    import opentracing
    from jaeger_client import Config

    config = Config(
      config={
          'sampler': {
              'type': 'const',
              'param': 1,
          },
          'logging': True,
      },
      service_name='somename',
    )
    
    opentracing_tracer = config.initialize_tracer()

  EOS
  code <<-EOS
  Tracing a method
  ────────────────────────────────────────
  ...
  def login():
    span = opentracing_tracer.start_span("validate_login")
    validate_login()
    span.finish()
    print('Login successful!')
  
  login()
  ...
  EOS
  code <<-EOS
  ┌─────────────────────────────┐
  │             \e[1mDemo\e[0m            │
  └─────────────────────────────┘
  EOS
end

section "\e[1mQuestions\e[0m" do
  center <<-EOS
    \e[1m
    ¡Thank you!
    \e[0m
    
    Demo code

    https://github.com/p404/opentracing-python-demo
    
    https://github.com/p404/jaeger-elasticsearch-compose
    \e[1m
    pablo[at]sequel[dot]ninja
    \e[0m
  EOS
end
