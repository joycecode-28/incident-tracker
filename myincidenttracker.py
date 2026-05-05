from flask import Flask, request, jsonify
import mysql.connector
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="incident_db")

db_cursor = db.cursor(dictionary=True)

app = Flask(__name__)
incidents=[]

@app.route('/incident', methods=['POST'])
def create_incident():
    #error handling
    try: 
        data = request.get_json()
        #validation
        if not data or not data.get("title") or not data.get("status"):
            return jsonify({"error": "Title and Status are required"}), 400

        query = "INSERT INTO incidents (title, status) VALUES (%s, %s)"
        values = (data.get("title"), data.get("status"))

        db_cursor.execute(query, values)
        db.commit()
        return jsonify({"message": "Incident created successfully"}), 201

    except Exception as e:
        return jsonify({"message": "Error creating incident"}), 500

@app.route('/incident', methods=['GET'])
def get_incident():
    db_cursor.execute("SELECT * FROM incidents")
    data = db_cursor.fetchall()
    
    return jsonify({
        "message": "Incidents retrieved successfully",
        "data": data
    }),200

@app.route('/incident/<int:id>', methods=['PUT'])
def update_incident(id):
    data = request.get_json()
    
    query = "UPDATE incidents SET title=%s, status=%s WHERE id=%s"
    values = (data.get("title"), data.get("status"), id)

    db_cursor.execute(query, values)
    db.commit()

    if db_cursor.rowcount == 0:
        return jsonify({"error": "Incident not found"}), 404
    
    return jsonify({"message": "Updated"}),200

@app.route('/incident/<int:id>', methods=['DELETE'])
def delete_incident(id):
    
    query = "DELETE FROM incidents WHERE id=%s"
    
    db_cursor.execute(query, (id,))
    db.commit()
    if db_cursor.rowcount == 0:
        return jsonify({"error": "Incident not found"}), 404

    return jsonify({
        "message": "Deleted"
    }),200

if __name__ == '__main__':
    app.run(debug=True)
