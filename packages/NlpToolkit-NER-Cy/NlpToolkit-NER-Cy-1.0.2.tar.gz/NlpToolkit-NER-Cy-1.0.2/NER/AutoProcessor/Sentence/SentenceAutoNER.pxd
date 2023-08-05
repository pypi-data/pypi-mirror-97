from NamedEntityRecognition.AutoNER cimport AutoNER
from AnnotatedSentence.AnnotatedSentence cimport AnnotatedSentence


cdef class SentenceAutoNER(AutoNER):

    cpdef autoDetectPerson(self, AnnotatedSentence sentence)
    cpdef autoDetectLocation(self, AnnotatedSentence sentence)
    cpdef autoDetectOrganization(self, AnnotatedSentence sentence)
    cpdef autoDetectMoney(self, AnnotatedSentence sentence)
    cpdef autoDetectTime(self, AnnotatedSentence sentence)
    cpdef autoNER(self, AnnotatedSentence sentence)
