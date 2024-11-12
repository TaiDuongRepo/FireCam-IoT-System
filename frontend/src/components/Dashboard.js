import React, { useState } from "react";

export default function Dashboard() {
    const [selectedCam, setSelectedCam] = useState(0);

    const handleCamClick = (camIndex) => {
        setSelectedCam(camIndex);
    };

    return (
        <div className="container mx-auto p-4">
            <header className="flex justify-between items-center mb-4 bg-blue-500 text-white p-4 rounded shadow">
                <div className="flex items-center">
                    <h1 className="text-2xl font-bold mr-4">Logo</h1>
                    <h2 className="text-xl">Camera {selectedCam !== null ? selectedCam : 0} - View</h2>
                </div>
                <div className="text-xl font-semibold" id="timer">01:02:03</div>
                <div className="flex items-center">
                    <input type="text" placeholder="Search camera..." className="border rounded-l px-2 py-1" />
                    <button className="bg-blue-500 text-white px-4 py-1 rounded-r"><i className="fa fa-search" aria-hidden="true"></i></button>
                </div>
            </header>

            <div className="grid grid-cols-4 gap-4 mb-4">
                {[0, 1, 2, 3].map((camIndex) => (
                    <div
                        key={camIndex}
                        className={`bg-white p-4 rounded shadow cursor-pointer ${selectedCam === camIndex ? 'border-2 border-blue-500' : ''}`}
                        onClick={() => handleCamClick(camIndex)}
                    >
                        <div className="text-center font-semibold">Camera {camIndex}</div>
                    </div>
                ))}
            </div>

            <div className="flex gap-4">
                <div className="w-3/4 bg-white p-4 rounded shadow">
                    <div className="mb-2 flex justify-end">
                        <span className="bg-gray-200 px-2 py-1 rounded">Camera {selectedCam !== null ? selectedCam : 0}</span>
                    </div>
                    <div className="aspect-video bg-gray-200 flex items-center justify-center">
                        <span className="text-lg font-semibold">Camera {selectedCam !== null ? selectedCam : 0}</span>
                    </div>
                </div>
                <div className="w-1/4 space-y-4">
                    <div className="bg-white p-4 rounded shadow">
                        <div className="flex mb-2">
                            <input type="text" placeholder="io adafruit key" className="border rounded-l px-2 py-1 flex-grow" />
                            <button className="bg-blue-500 text-white px-4 py-1 rounded-r">Connect</button>
                        </div>
                    </div>
                    <div className="bg-white p-4 rounded shadow h-64">
                        <h3 className="font-semibold mb-2">Logs</h3>
                        <div className="bg-gray-200 flex items-center justify-center"></div>
                    </div>
                </div>
            </div>
        </div>
    );
}