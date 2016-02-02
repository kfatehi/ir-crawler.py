package ir.analysis;

import ir.analysis.Frequency;
import ir.analysis.Utilities;
import ir.analysis.db.Database;

import java.io.File;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Collections;
import java.util.HashSet;

import java.sql.*;
import java.net.URI;

public final class FindSubDomains {
	/**
	 * Loops through every page's text content to determine word frequencies.
	 * 
	 * @param args The first element should contain the path to a text file.
	 */
	public static void main(String[] args) {
		Database.configure();
		try {
			Connection con = Database.conn;
			PreparedStatement st = con.prepareStatement(
					"SELECT url FROM PAGES");
			ResultSet rs = st.executeQuery();

			HashMap<String, Frequency> subdomains = new HashMap();

			while (rs.next()) {
				String url = rs.getString(1);
				try {
					URI uri = URI.create(url);
					String host = uri.getHost();
					Frequency freq = subdomains.getOrDefault(host, new Frequency(host));

					freq.incrementFrequency();
					subdomains.put(host, freq);
				} catch (Exception e) {
					//
				}
			}

			ArrayList<Frequency> freqs = new ArrayList<>(subdomains.values());
			Collections.sort(freqs, Utilities.frequencyComparator);
			Utilities.printFrequencies(freqs, "%s, %d%n");

			st.close();
		} catch(SQLException e) {
			System.out.println("oops");
		}
	}
}
