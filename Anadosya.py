import cv2
import dlib
import face_recognition
from datetime import datetime
import sqlite3
con=sqlite3.connect("taninanlariyaz.db")
cursor=con.cursor()

def tablo():
    cursor.execute("create table if not exists KISILER(ad TEXT, zaman DATETIME)")
    con.commit()
tablo()

def ekle(isim,tarih):
    cursor.execute("Insert into KISILER Values(?,?)",(isim,tarih))
    con.commit()

detector=dlib.get_frontal_face_detector()

mert=face_recognition.load_image_file("mert.jpeg")
mert_kodlama=face_recognition.face_encodings(mert)[0]
fatih=face_recognition.load_image_file("fatih.jpg")
fatih_kodlama=face_recognition.face_encodings(fatih)[0]
halil=face_recognition.load_image_file("halil.jpg")
halil_kodlama=face_recognition.face_encodings(halil)[0]


cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()

    yuz_lokasyonu=[]
    faces=detector(frame)
    for face in  faces:
        x=face.left()
        y=face.top()
        w=face.right()
        h=face.bottom()
        yuz_lokasyonu.append((y,w,h,x))
    face_kodlama1=face_recognition.face_encodings(frame,yuz_lokasyonu)

    i=0

    for face in face_kodlama1:
        y, w, h, x=yuz_lokasyonu[i]


        sonuc=face_recognition.compare_faces([mert_kodlama],face)

        sonuc2 = face_recognition.compare_faces([fatih_kodlama], face)
        sonuc3 = face_recognition.compare_faces([halil_kodlama], face)
        if sonuc[0]==True:
            cv2.rectangle(frame,(x,y),(w,h),(255,0,0),2)
            cv2.putText(frame,"Mert",(x,h+17),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),4)
            ekle("Mert",datetime.now())

        elif sonuc2[0] == True:
            cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 2)
            cv2.putText(frame, "Fatih", (x, h + 17), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
            ekle("Fatih", datetime.now())
        elif sonuc3[0] == True:
            cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 2)
            cv2.putText(frame, "Halil", (x, h + 17), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
            ekle("Halil", datetime.now())
        else:
            cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 2)
            cv2.putText(frame, "Tanimlanamadi", (x, h + 17), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)
            ekle("Tanimlanamadi", datetime.now())

    cv2.imshow("Pencere",frame)
    if cv2.waitKey(10) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

con.close()