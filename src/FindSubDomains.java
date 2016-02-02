package ir.analysis;

import ir.analysis.Frequency;
import ir.analysis.Utilities;
import ir.analysis.db.Database;

import java.io.File;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Collections;

import java.sql.*;

public final class FindSubDomains {
	/**
	 * Loops through every page's text content to determine word frequencies.
	 * 
	 * @param args The first element should contain the path to a text file.
	 */
	public static void main(String[] args) {
		HashMap<String,Frequency> map = new HashMap<>();
		Database.configure();
		try {
			Connection con = Database.conn;
			PreparedStatement st = con.prepareStatement(
					"SELECT text FROM PAGES "
				   	+"WHERE TEXT IS NOT NULL LIMIT 10");
			ResultSet rs = st.executeQuery();

			while (rs.next()) {
				String text = rs.getString(1);
					List<String> words = Utilities.tokenizeString(text);
					WordFrequencyCounter.computeWordFrequencies(words, map);
			}

			ArrayList<Frequency> freqs = new ArrayList<>(map.values());
			Collections.sort(freqs, Utilities.frequencyComparator);
			Utilities.printFrequencies(freqs);

			st.close();
		} catch(SQLException e) {
			System.out.println("oops");
		}
	}
}
